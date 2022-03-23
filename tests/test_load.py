from ziptool import load

def test_load_crosswalk():
    df = load.load_crosswalk()
    assert "zip" in df.columns
    assert len(df) == 172177
