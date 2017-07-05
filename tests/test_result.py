from hathi_validate import result


def test_summary_builder():
    summary_builder = result.SummaryDirector(source="spam")
    summary_builder.add_error("Not valid")
    summary = summary_builder.construct()
    assert isinstance(summary, result.ResultSummary)