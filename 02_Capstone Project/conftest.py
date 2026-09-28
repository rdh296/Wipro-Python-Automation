import os

import pytest
import yaml

from framework.driver_factory import create_driver
from framework.logger import get_logger


logger = get_logger()


# ==========================================================
# CONFIGURATION
# ==========================================================

def load_config():

    with open(
        "config/config.yaml",
        "r",
        encoding="utf-8"
    ) as file:

        return yaml.safe_load(file)


# ==========================================================
# CONFIG FIXTURE
# ==========================================================

@pytest.fixture
def config():

    logger.info(
        "Loading configuration"
    )

    return load_config()


# ==========================================================
# DRIVER FIXTURE
# ==========================================================

@pytest.fixture
def driver(config):

    logger.info(
        "Starting browser"
    )

    driver = create_driver(
        config
    )

    logger.info(
        "Browser started successfully"
    )

    yield driver

    logger.info(
        "Closing browser"
    )

    driver.quit()


# ==========================================================
# ADAPTIVEQA TEST REPORT DATA
# ==========================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    # We only need the actual test execution result
    if report.when != "call":
        return

    # Get Selenium driver
    driver = item.funcargs.get("driver")

    # If this test does not use Selenium driver
    if driver is None:
        report.adaptiveqa_status = "N/A"
        report.adaptiveqa_events = []
        return

    # Get AdaptiveQA healer
    healer = getattr(
        driver,
        "_adaptiveqa_healer",
        None
    )

    # ======================================================
    # NO HEALER
    # ======================================================

    if healer is None:

        if report.failed:
            status = "FAILED"
        else:
            status = "STABLE"

        report.adaptiveqa_status = status
        report.adaptiveqa_events = []

        return

    # ======================================================
    # GET EVENTS
    # ======================================================

    events = healer.events

    report.adaptiveqa_events = events

    # ======================================================
    # DETERMINE HEALTH
    # ======================================================

    if any(
        event["status"] == "FAILED"
        for event in events
    ):

        status = "FAILED"

    elif any(
        event["status"] == "HEALED"
        for event in events
    ):

        status = "HEALED"

    else:

        status = "STABLE"

    report.adaptiveqa_status = status

    # ======================================================
    # RETRY COUNT
    # ======================================================

    report.adaptiveqa_retry_count = getattr(
        report,
        "rerun",
        0
    )

    # ======================================================
    # BUILD DETAILS FOR TEST REPORT
    # ======================================================

    locator_rows = ""

    for event in events:

        event_status = event["status"]

        original = str(
            event["original_locator"]
        )

        recovered = event[
            "recovered_locator"
        ]

        attempts = event[
            "attempts"
        ]

        if recovered is None:

            recovered_text = "N/A"

        else:

            recovered_text = str(
                recovered
            )

        locator_rows += f"""
        <tr>

            <td>
                <b>{event_status}</b>
            </td>

            <td>
                {original}
            </td>

            <td>
                {recovered_text}
            </td>

            <td>
                {attempts}
            </td>

        </tr>
        """

    # ======================================================
    # ADAPTIVEQA DETAILS HTML
    # ======================================================

    adaptiveqa_html = f"""
    <div style="
        border: 2px solid #444;
        padding: 15px;
        margin: 15px 0;
        border-radius: 8px;
        background: #f8f8f8;
    ">

        <h2>
            AdaptiveQA Intelligence
        </h2>

        <p>
            <b>Locator Health:</b>
            {status}
        </p>

        <p>
            <b>Test Result:</b>
            {report.outcome.upper()}
        </p>

        <p>
            <b>Retry Count:</b>
            {getattr(report, "rerun", 0)}
        </p>

        <h3>
            Locator Recovery Details
        </h3>

        <table
            border="1"
            cellpadding="8"
            cellspacing="0"
            style="
                border-collapse: collapse;
                width: 100%;
            "
        >

            <tr>

                <th>
                    Status
                </th>

                <th>
                    Original Locator
                </th>

                <th>
                    Recovered Locator
                </th>

                <th>
                    Attempts
                </th>

            </tr>

            {locator_rows}

        </table>

    </div>
    """

    # ======================================================
    # ADD DETAILS TO PYTEST HTML
    # ======================================================

    try:

        extra = getattr(
            report,
            "extras",
            []
        )

        extra.append(
            pytest_html.extras.html(
                adaptiveqa_html
            )
        )

        report.extras = extra

    except Exception as error:

        logger.error(
            "Could not add AdaptiveQA HTML: %s",
            error
        )

    # ======================================================
    # SCREENSHOT ON FAILURE
    # ======================================================

    if report.failed:

        os.makedirs(
            "screenshots",
            exist_ok=True
        )

        screenshot_path = (
            f"screenshots/"
            f"{item.name}_report.png"
        )

        try:

            driver.save_screenshot(
                screenshot_path
            )

            extra = getattr(
                report,
                "extras",
                []
            )

            extra.append(
                pytest_html.extras.image(
                    screenshot_path
                )
            )

            report.extras = extra

            logger.info(
                "AdaptiveQA screenshot created: %s",
                screenshot_path
            )

        except Exception as error:

            logger.error(
                "AdaptiveQA screenshot failed: %s",
                error
            )


# ==========================================================
# ADD ADAPTIVEQA COLUMN TO MAIN HTML REPORT
# ==========================================================

def pytest_html_results_table_header(cells):

    cells.insert(
        2,
        "AdaptiveQA Health"
    )


# ==========================================================
# ADD HEALTH STATUS TO EACH TEST ROW
# ==========================================================

def pytest_html_results_table_row(report, cells):

    status = getattr(
        report,
        "adaptiveqa_status",
        "N/A"
    )

    cells.insert(
        2,
        status
    )


# ==========================================================
# ADD ADAPTIVEQA SUMMARY TO REPORT
# ==========================================================

def pytest_html_results_summary(
    prefix,
    summary,
    postfix
):

    prefix.extend([
        """
        <h2>
            AdaptiveQA Automation Health
        </h2>

        <p>
            <b>STABLE</b> =
            Primary locator worked successfully.
        </p>

        <p>
            <b>HEALED</b> =
            Primary locator failed and
            AdaptiveQA recovered using a
            fallback locator.
        </p>

        <p>
            <b>FAILED</b> =
            Primary and fallback locators
            could not locate the element.
        </p>
        """
    ])