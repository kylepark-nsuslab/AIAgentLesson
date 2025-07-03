"""
보안 설정 테스트
"""

import os
from django.test import TestCase, override_settings
from django.test.client import Client
from django.core.management import execute_from_command_line
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from memos.models import Memo


class SecuritySettingsTest(TestCase):
    """보안 설정 테스트"""
    
    def test_signup_redirect_after_registration(self):
        """회원가입 후 올바른 페이지로 리다이렉트 되는지 테스트"""
        response = self.client.post('/signup/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'complex_password123',
            'password2': 'complex_password123',
        })
        # 회원가입 후 메모 목록 페이지로 리다이렉트
        self.assertRedirects(response, '/')
        
        # 사용자가 실제로 로그인되었는지 확인
        self.assertIn('_auth_user_id', self.client.session)
        
        # 새 사용자가 생성되었는지 확인
        self.assertTrue(User.objects.filter(username='newuser').exists())

    @override_settings(
        DEBUG=False,
        SECRET_KEY='test-very-long-and-secure-secret-key-for-testing-purposes-only',
        USE_HTTPS=True,
        SECURE_SSL_REDIRECT=True,
        SECURE_HSTS_SECONDS=31536000,
        SESSION_COOKIE_SECURE=True,
        CSRF_COOKIE_SECURE=True,
        SECURE_CONTENT_TYPE_NOSNIFF=True,
        SECURE_BROWSER_XSS_FILTER=True,
        X_FRAME_OPTIONS='DENY',
        SESSION_COOKIE_HTTPONLY=True,
        CSRF_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Strict',
        CSRF_COOKIE_SAMESITE='Strict'
    )
    def test_production_security_settings(self):
        """프로덕션 보안 설정이 올바르게 적용되는지 테스트"""
        from django.conf import settings
        
        # 보안 설정들이 올바르게 설정되었는지 확인
        self.assertFalse(settings.DEBUG)
        self.assertTrue(settings.SECURE_SSL_REDIRECT)
        self.assertEqual(settings.SECURE_HSTS_SECONDS, 31536000)
        self.assertTrue(settings.SESSION_COOKIE_SECURE)
        self.assertTrue(settings.CSRF_COOKIE_SECURE)
        self.assertTrue(settings.SECURE_CONTENT_TYPE_NOSNIFF)
        self.assertTrue(settings.SECURE_BROWSER_XSS_FILTER)
        self.assertEqual(settings.X_FRAME_OPTIONS, 'DENY')
        self.assertTrue(settings.SESSION_COOKIE_HTTPONLY)
        self.assertTrue(settings.CSRF_COOKIE_HTTPONLY)
        self.assertEqual(settings.SESSION_COOKIE_SAMESITE, 'Strict')
        self.assertEqual(settings.CSRF_COOKIE_SAMESITE, 'Strict')

    def test_password_validation_strength(self):
        """패스워드 검증 강도 테스트"""
        # 너무 짧은 패스워드로 회원가입 시도
        response = self.client.post('/signup/', {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password1': '123',  # 너무 짧음
            'password2': '123',
        })
        # 회원가입이 실패해야 함
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser2').exists())
        
        # 일반적인 패스워드로 회원가입 시도
        response = self.client.post('/signup/', {
            'username': 'testuser3',
            'email': 'test3@example.com',
            'password1': 'password',  # 너무 일반적
            'password2': 'password',
        })
        # 회원가입이 실패해야 함
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser3').exists())

    def test_user_isolation_security(self):
        """사용자 격리 보안 테스트"""
        # 두 명의 사용자 생성
        user1 = User.objects.create_user('user1', 'user1@test.com', 'password123')
        user2 = User.objects.create_user('user2', 'user2@test.com', 'password123')
        
        # user1의 메모 생성
        memo1 = Memo.objects.create(user=user1, title='User1 Memo', content='Private content')
        
        # user2로 로그인
        self.client.login(username='user2', password='password123')
        
        # user1의 메모에 직접 접근 시도
        response = self.client.get(f'/memo/{memo1.pk}/')
        self.assertEqual(response.status_code, 404)  # 접근 불가
        
        # user1의 메모 수정 시도
        response = self.client.get(f'/memo/{memo1.pk}/edit/')
        self.assertEqual(response.status_code, 404)  # 수정 불가
        
        # user1의 메모 삭제 시도
        response = self.client.post(f'/memo/{memo1.pk}/delete/')
        self.assertEqual(response.status_code, 404)  # 삭제 불가
        
        # 메모가 여전히 존재하는지 확인
        self.assertTrue(Memo.objects.filter(pk=memo1.pk).exists())