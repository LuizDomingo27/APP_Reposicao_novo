# ═══════════════════════════════════════════════════════════════════════════════
# ROBUST TEST RUNNER — Executes full suite of unit & integration tests
# (Works natively with built-in unittest, and supports pytest if installed)
# ═══════════════════════════════════════════════════════════════════════════════

import sys
import unittest
from pathlib import Path

# Ensure project root is in sys.path
ROOT_DIR = str(Path(__file__).resolve().parent)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


def run():
    print("=" * 70)
    print("EXECUTANDO SUÍTE DE TESTES ROBUSTOS — GESTÃO DE REPOSIÇÕES")
    print("=" * 70)

    # Use standard library unittest discovery (zero dependencies required)
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    if result.wasSuccessful():
        print(f"SUCESSO: {result.testsRun} testes executados com êxito! (0 falhas, 0 erros)")
        print("=" * 70)
        sys.exit(0)
    else:
        print(f"FALHA: {len(result.failures)} falha(s), {len(result.errors)} erro(s) encontrados.")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    run()
