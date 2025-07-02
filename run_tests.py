#!/usr/bin/env python
"""
테스트 실행 스크립트
메모장 애플리케이션의 모든 테스트를 실행하고 결과를 출력합니다.
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'memoapp.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    print("=" * 60)
    print("메모장 애플리케이션 테스트 실행")
    print("=" * 60)
    
    # 모든 테스트 실행
    failures = test_runner.run_tests(["memos.tests"])
    
    print("\n" + "=" * 60)
    if failures:
        print(f"테스트 실패: {failures}개")
        sys.exit(1)
    else:
        print("모든 테스트 통과!")
        print("=" * 60)