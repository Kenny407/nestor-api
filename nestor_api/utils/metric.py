"""A simple metric implementation awaiting for proper implementation"""


class Metric:  # pylint: disable=too-few-public-methods
    """A fake metric module to be able to create dashboard later on"""
    stats = dict()

    @staticmethod
    def increment(stat_name: str) -> None:
        """Increment a stat"""
        current_value = Metric.stats.get(stat_name, 0)
        Metric.stats[stat_name] = current_value + 1
