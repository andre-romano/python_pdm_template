import pytest
from python_pdm_template.core.parsers.apache_parser import ApacheParser, ParseError

def test_apache_parser_combined_format():
    parser = ApacheParser()
    linha_combined = '127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326 "http://www.example.com/" "Mozilla/4.08"'
    
    entry = parser.parse_line(linha_combined, 1)
    
    assert entry.ip == "127.0.0.1"
    assert entry.method == "GET"
    assert entry.status == 200
    assert entry.referer == "http://www.example.com/"

def test_apache_parser_common_format():
    parser = ApacheParser()
    linha_common = '127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326'
    
    entry = parser.parse_line(linha_common, 2)
    
    assert entry.ip == "127.0.0.1"
    assert entry.method == "GET"
    assert entry.status == 200
    assert entry.referer is None

def test_apache_parser_linha_malformada():
    parser = ApacheParser()
    linha_invalida = 'Essa linha não é um log do Apache'
    
    with pytest.raises(ParseError) as exc_info:
        parser.parse_line(linha_invalida, 3)
        
    assert "linha 3" in str(exc_info.value)