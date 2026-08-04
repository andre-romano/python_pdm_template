
from python_pdm_template.__main__ import main

def test_main_executa_sem_erro():
    try:
        main()
    except SystemExit:
        pass  
    except Exception as e:
        assert False, f"main() lançou exceção inesperada: {e}"
