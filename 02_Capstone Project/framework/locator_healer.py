from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from framework.logger import get_logger


logger = get_logger()


class LocatorHealer:

    def __init__(self, driver, wait):

        self.driver = driver
        self.wait = wait

        # ==================================================
        # CURRENT LOCATOR STATUS
        # ==================================================

        self.healed = False

        self.original_locator = None

        self.recovered_locator = None

        # ==================================================
        # ADAPTIVEQA EVENT HISTORY
        # ==================================================
        #
        # This stores every locator event during the test.
        #
        # Example:
        #
        # [
        #     {
        #         "status": "STABLE",
        #         "original_locator": ("id", "input-email"),
        #         "recovered_locator": None,
        #         "attempts": 0
        #     }
        # ]
        #
        # Or:
        #
        # [
        #     {
        #         "status": "HEALED",
        #         "original_locator": ("id", "wrong-id"),
        #         "recovered_locator": ("id", "input-email"),
        #         "attempts": 1
        #     }
        # ]
        #

        self.events = []

    # ======================================================
    # FIND ELEMENT USING ADAPTIVEQA
    # ======================================================

    def find(self, locator, alternatives=None):

        # --------------------------------------------------
        # Reset current locator information
        # --------------------------------------------------

        self.original_locator = locator

        self.healed = False

        self.recovered_locator = None

        # Make sure alternatives is always a list
        alternatives = alternatives or []

        # ==================================================
        # STEP 1
        # TRY PRIMARY LOCATOR
        # ==================================================

        try:

            element = self.wait.until(
                EC.visibility_of_element_located(
                    locator
                )
            )

            # --------------------------------------------------
            # PRIMARY LOCATOR WORKED
            # --------------------------------------------------

            self.events.append({
                "status": "STABLE",
                "original_locator": locator,
                "recovered_locator": None,
                "attempts": 0
            })

            logger.info(
                "AdaptiveQA: Locator STABLE | %s",
                locator
            )

            return element

        except TimeoutException:

            logger.warning(
                "AdaptiveQA: Primary locator failed | %s",
                locator
            )

        # ==================================================
        # STEP 2
        # TRY FALLBACK LOCATORS
        # ==================================================

        for attempt_number, alternative in enumerate(
            alternatives,
            start=1
        ):

            try:

                logger.warning(
                    "AdaptiveQA: Trying fallback locator "
                    "%s | %s",
                    attempt_number,
                    alternative
                )

                element = self.wait.until(
                    EC.visibility_of_element_located(
                        alternative
                    )
                )

                # --------------------------------------------------
                # FALLBACK LOCATOR WORKED
                # --------------------------------------------------

                self.healed = True

                self.recovered_locator = alternative

                self.events.append({
                    "status": "HEALED",
                    "original_locator": locator,
                    "recovered_locator": alternative,
                    "attempts": attempt_number
                })

                logger.warning(
                    "AdaptiveQA: SELF-HEAL SUCCESS | "
                    "Original: %s | "
                    "Recovered: %s | "
                    "Attempts: %s",
                    locator,
                    alternative,
                    attempt_number
                )

                return element

            except TimeoutException:

                logger.warning(
                    "AdaptiveQA: Fallback locator failed | "
                    "%s",
                    alternative
                )

        # ==================================================
        # STEP 3
        # ALL LOCATORS FAILED
        # ==================================================

        self.events.append({
            "status": "FAILED",
            "original_locator": locator,
            "recovered_locator": None,
            "attempts": len(alternatives)
        })

        logger.error(
            "AdaptiveQA: SELF-HEAL FAILED | "
            "Original: %s | "
            "Fallback attempts: %s",
            locator,
            len(alternatives)
        )

        # --------------------------------------------------
        # Raise exception so PyTest marks the test failed
        # --------------------------------------------------

        raise TimeoutException(
            "AdaptiveQA could not find element. "
            f"Original locator: {locator}. "
            f"Fallback attempts: {len(alternatives)}"
        )