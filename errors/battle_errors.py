class BattleTimeoutError(RuntimeError):
    """Raised when a battle does not finish within max_duration."""
    def __init__(
        self,
        duration,
        latched_hp=None,
        latched_killed_percent=None,
        mode=None,
        level=None,
    ):
        self.duration = duration
        self.latched_hp = latched_hp
        self.latched_killed_percent = latched_killed_percent
        self.mode = mode
        self.level = level

        super().__init__(
            f"Battle timeout after {duration:.1f}s "
            f"(hp={latched_hp}, killed={latched_killed_percent}%, "
            f"mode={mode}, level={level})"
        )