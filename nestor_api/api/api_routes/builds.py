"""Define the builds route."""
from http import HTTPStatus
from flask import Blueprint, Response

from nestor_api.utils.logger import Logger
from nestor_api.utils.metric import Metric
from nestor_api.lib.app import get_version

import nestor_api.lib.config as config
import nestor_api.lib.docker as docker
import nestor_api.lib.git as git
import nestor_api.lib.io as io


def register_routes(api: Blueprint) -> None:
    """Register the /builds routes."""

    @api.route("/builds/<app>", methods=["POST"])
    def _sample(app) -> Response:
        """Builds the docker image of an application from the master branch with a unique tag and
        upload it to the configured Docker registry."""

        Logger.info({"app": app}, "[/api/builds/:app] Building an application")
        Metric.increment(f"build.{app}.started")

        # TODO awaiting for implementation
        # Respond here that we accept the request to have an asynchronous hook (non-blocking)

        working_dir = None
        config_dir = None

        try:
            config_dir = config.get_configuration_copy_path()

            Logger.debug(
                {app, config_dir}, "[/api/builds/:app] Changing environment to staging",
            )
            config.change_environment("staging", config_dir)

            working_dir = git.create_working_repository(app, config_dir)
            Logger.debug({app, working_dir}, "[/api/builds/:app] Working directory")

            tag = None

            try:
                Metric.increment(f"build.{app}.tags.creation.started")

                Logger.info(
                    {app}, "[/api/builds/:app] Start tagging and building Docker image",
                )
                version = get_version(working_dir)

                tag = git.tag(working_dir, app, version, config_dir)

                Logger.info({tag, app}, "[/api/builds/:app] Tag created")

                Metric.increment(f"build.{app}.tags.creation.success")
            except Exception as err:  # pylint: disable=broad-except
                # Tag might already exists
                Logger.warn({err}, "[/api/builds/:app] Error while tagging the app")

                Metric.increment(f"build.{app}.tags.creation.failed")

            Logger.info({app}, "[/api/builds/:app] building Docker image")

            try:
                Metric.increment(f"build.{app}.docker.build.started")

                docker.build(
                    app, {"repository": working_dir, "config_path": config_dir},
                )

                Metric.increment(f"build.{app}.docker.build.success")
            except Exception: # pylint: disable=broad-except
                Metric.increment(f"build.{app}.docker.build.failed")
                raise RuntimeError("Docker build failed")

            Metric.increment(f"build.{app}.docker.upload.started")

            docker.push(app, working_dir, config_dir)
            Logger.info({app}, "[/api/builds/:app] Docker image uploaded")

            Metric.increment(f"build.{app}.docker.upload.success")

            Metric.increment(f"build.{app}.tags.push.started")

            git.push(working_dir)
            Logger.info({app}, "[/api/builds/:app] Git tag pushed")

            Metric.increment(f"build.{app}.tags.push.success")

            # TODO make the workflow go one step further here
            # Investigate this

        except Exception as err: # pylint: disable=broad-except
            Logger.error(
                {"app": app, "err": err},
                "[/api/builds/:app] Error while tagging and building the app",
            )
            Metric.increment(f"build.{app}.failed")

        # Clean up
        try:
            if working_dir:
                io.remove(working_dir)

            if config_dir:
                io.remove(config_dir)

        except Exception as err: # pylint: disable=broad-except
            Logger.error({"err": err}, "[/api/builds/:app] Error during clean up")

        return "", HTTPStatus.ACCEPTED
