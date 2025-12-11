"""Pytest configuration and fixtures for PMM Agent tests."""

import pytest
import os

# Set test environment
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")


@pytest.fixture
def sample_homepage_content():
    """Sample homepage content for testing PMM evaluation tools."""
    return """
    <html>
    <head><title>Acme Corp - Enterprise Solutions</title></head>
    <body>
        <h1>Welcome to Acme Corp</h1>
        <p>We provide solutions for your business needs.</p>
        <a href="/contact">Contact Us</a>
    </body>
    </html>
    """


@pytest.fixture
def good_homepage_content():
    """Well-structured homepage content that should pass PMM tests."""
    return """
    <html>
    <head><title>CashIsClay - Train Your Team to Ship AI in 48 Hours</title></head>
    <body>
        <h1>Train your team to ship AI in 48 hours, not 6 months.</h1>
        <p>Become the AI leader your organization needs. Learn the $30K/month methodology.</p>
        <p>For: Professionals who want to become their team's AI expert</p>
        <p>Unlike certification programs that teach theory, we train you to actually ship.</p>
        <a href="/join">Join the Next Cohort - $2,197</a>
    </body>
    </html>
    """
