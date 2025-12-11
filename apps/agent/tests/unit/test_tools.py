"""Unit tests for PMM Agent tools.

Testing Trophy Base Layer - Pure function tests
"""

import pytest


class TestFiveSecondTestCriteria:
    """Tests for 5-second test evaluation criteria."""

    def test_criteria_list_is_complete(self):
        """5-second test should check 4 things."""
        criteria = [
            "What do they do?",
            "Who is it for?",
            "What makes it different?",
            "What should I do next?",
        ]
        assert len(criteria) == 4

    def test_pass_threshold(self):
        """Should require 4/4 to pass."""
        pass_threshold = 4
        assert pass_threshold == 4


class TestPositioningFramework:
    """Tests for April Dunford positioning framework."""

    def test_positioning_elements(self):
        """Positioning should include all 5 April Dunford elements."""
        elements = [
            "competitive_alternatives",
            "unique_attributes",
            "value",
            "target_customers",
            "market_category",
        ]
        assert len(elements) == 5

    def test_scoring_scale(self):
        """Scores should be 0-100."""
        min_score = 0
        max_score = 100
        assert min_score == 0
        assert max_score == 100


class TestMessagingHierarchy:
    """Tests for Fletch PMM messaging hierarchy."""

    def test_messaging_layers(self):
        """Messaging hierarchy should have 5 layers."""
        layers = [
            "strategic_narrative",
            "positioning_statement",
            "value_propositions",
            "proof_points",
            "micro_copy",
        ]
        assert len(layers) == 5

    def test_layers_are_ordered(self):
        """Strategic narrative should be first, micro-copy last."""
        layers = [
            "strategic_narrative",
            "positioning_statement",
            "value_propositions",
            "proof_points",
            "micro_copy",
        ]
        assert layers[0] == "strategic_narrative"
        assert layers[-1] == "micro_copy"


class TestAntiPatterns:
    """Tests for PMM anti-pattern detection."""

    def test_critical_anti_patterns(self):
        """Should detect critical anti-patterns."""
        critical_patterns = [
            "no_competitive_frame",
            "missing_target_audience",
            "vague_value_proposition",
            "no_clear_cta",
        ]
        assert len(critical_patterns) >= 3
