def test_ensure_output_dir(tmp_path):
    """Test output directory creation."""
    # Test directory creation
    test_dir = tmp_path / "test_output"
    ensure_output_dir(str(test_dir))
    assert test_dir.exists()
    
    # Test existing directory
    ensure_output_dir(str(test_dir))
    assert test_dir.exists()
    
    # Test nested directory
    nested_dir = test_dir / "nested" / "dir"
    ensure_output_dir(str(nested_dir))
    assert nested_dir.exists()

def test_clean_filename_edge_cases():
    """Test filename cleaning with edge cases."""
    # Test long filename
    long_filename = "a" * 255 + ".txt"
    cleaned = clean_filename(long_filename)
    assert len(cleaned) <= 255
    
    # Test international characters
    assert clean_filename("übér jöb.txt") == "übér_jöb.txt"
    
    # Test leading/trailing spaces
    assert clean_filename(" job post .txt ") == "job_post_.txt"