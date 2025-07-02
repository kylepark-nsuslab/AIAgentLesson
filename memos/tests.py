from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Memo
from .forms import SignUpForm, MemoForm


class TestMemoModel(TestCase):
    """메모 모델 테스트"""
    
    def setUp(self):
        """테스트 데이터 초기화"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
    
    def test_memo_creation(self):
        """메모 생성 테스트"""
        memo = Memo.objects.create(
            user=self.user,
            title='테스트 메모',
            content='테스트 내용입니다.'
        )
        self.assertEqual(memo.title, '테스트 메모')
        self.assertEqual(memo.content, '테스트 내용입니다.')
        self.assertEqual(memo.user, self.user)
        self.assertIsNotNone(memo.created_at)
        self.assertIsNotNone(memo.updated_at)
    
    def test_memo_str_method(self):
        """메모 __str__ 메서드 테스트"""
        memo = Memo.objects.create(
            user=self.user,
            title='테스트 제목',
            content='테스트 내용'
        )
        self.assertEqual(str(memo), '테스트 제목')
    
    def test_memo_user_relationship(self):
        """메모와 사용자 관계 테스트"""
        memo = Memo.objects.create(
            user=self.user,
            title='관계 테스트',
            content='관계 테스트 내용'
        )
        self.assertIn(memo, self.user.memos.all())


class TestSignUpForm(TestCase):
    """회원가입 폼 테스트"""
    
    def test_valid_form(self):
        """유효한 폼 데이터 테스트"""
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form_password_mismatch(self):
        """비밀번호 불일치 폼 테스트"""
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'testpassword123',
            'password2': 'differentpassword',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_invalid_form_missing_email(self):
        """이메일 누락 폼 테스트"""
        form_data = {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestMemoForm(TestCase):
    """메모 폼 테스트"""
    
    def test_valid_memo_form(self):
        """유효한 메모 폼 테스트"""
        form_data = {
            'title': '테스트 제목',
            'content': '테스트 내용입니다.'
        }
        form = MemoForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_memo_form_empty_title(self):
        """제목 없는 메모 폼 테스트"""
        form_data = {
            'title': '',
            'content': '테스트 내용입니다.'
        }
        form = MemoForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_invalid_memo_form_empty_content(self):
        """내용 없는 메모 폼 테스트"""
        form_data = {
            'title': '테스트 제목',
            'content': ''
        }
        form = MemoForm(data=form_data)
        self.assertFalse(form.is_valid())


class TestAuthViews(TestCase):
    """인증 관련 뷰 테스트"""
    
    def test_signup_get(self):
        """회원가입 페이지 GET 요청 테스트"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
    
    def test_signup_post_valid(self):
        """유효한 회원가입 POST 요청 테스트"""
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())
    
    def test_signup_post_invalid(self):
        """유효하지 않은 회원가입 POST 요청 테스트"""
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'differentpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser').exists())
    
    def test_login_valid(self):
        """유효한 로그인 테스트"""
        User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)
    
    def test_login_invalid(self):
        """유효하지 않은 로그인 테스트"""
        User.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)


class TestMemoViews(TestCase):
    """메모 관련 뷰 테스트"""
    
    def setUp(self):
        """테스트 사용자 및 메모 데이터 초기화"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpassword123'
        )
        self.memo = Memo.objects.create(
            user=self.user,
            title='테스트 메모',
            content='테스트 내용입니다.'
        )
    
    def test_memo_list_requires_login(self):
        """메모 목록 로그인 필수 테스트"""
        response = self.client.get(reverse('memo_list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/')
    
    def test_memo_list_authenticated(self):
        """로그인한 사용자의 메모 목록 테스트"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('memo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 메모')
    
    def test_memo_list_only_user_memos(self):
        """사용자별 메모 목록 분리 테스트"""
        # 다른 사용자의 메모 생성
        Memo.objects.create(
            user=self.other_user,
            title='다른 사용자 메모',
            content='다른 사용자 내용'
        )
        
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('memo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 메모')
        self.assertNotContains(response, '다른 사용자 메모')
    
    def test_memo_detail_authenticated(self):
        """로그인한 사용자의 메모 상세 테스트"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('memo_detail', args=[self.memo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 메모')
        self.assertContains(response, '테스트 내용입니다.')
    
    def test_memo_detail_wrong_user(self):
        """다른 사용자의 메모 접근 테스트"""
        self.client.login(username='otheruser', password='otherpassword123')
        response = self.client.get(reverse('memo_detail', args=[self.memo.pk]))
        self.assertEqual(response.status_code, 404)
    
    def test_memo_create_get(self):
        """메모 생성 페이지 GET 요청 테스트"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('memo_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
    
    def test_memo_create_post_valid(self):
        """유효한 메모 생성 POST 요청 테스트"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('memo_create'), {
            'title': '새 메모',
            'content': '새 메모 내용입니다.'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Memo.objects.filter(title='새 메모').exists())
        new_memo = Memo.objects.get(title='새 메모')
        self.assertEqual(new_memo.user, self.user)
    
    def test_memo_create_post_invalid(self):
        """유효하지 않은 메모 생성 POST 요청 테스트"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('memo_create'), {
            'title': '',
            'content': '내용만 있는 메모'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Memo.objects.filter(content='내용만 있는 메모').exists())
    
    def test_memo_update_get(self):
        """메모 수정 페이지 GET 요청 테스트"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('memo_update', args=[self.memo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 메모')
        self.assertContains(response, '테스트 내용입니다.')
    
    def test_memo_update_post_valid(self):
        """유효한 메모 수정 POST 요청 테스트"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('memo_update', args=[self.memo.pk]), {
            'title': '수정된 메모',
            'content': '수정된 내용입니다.'
        })
        self.assertEqual(response.status_code, 302)
        updated_memo = Memo.objects.get(pk=self.memo.pk)
        self.assertEqual(updated_memo.title, '수정된 메모')
        self.assertEqual(updated_memo.content, '수정된 내용입니다.')
    
    def test_memo_update_wrong_user(self):
        """다른 사용자의 메모 수정 시도 테스트"""
        self.client.login(username='otheruser', password='otherpassword123')
        response = self.client.get(reverse('memo_update', args=[self.memo.pk]))
        self.assertEqual(response.status_code, 404)
    
    def test_memo_delete_get(self):
        """메모 삭제 확인 페이지 GET 요청 테스트"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('memo_delete', args=[self.memo.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 메모')
    
    def test_memo_delete_post(self):
        """메모 삭제 POST 요청 테스트"""
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.post(reverse('memo_delete', args=[self.memo.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Memo.objects.filter(pk=self.memo.pk).exists())
    
    def test_memo_delete_wrong_user(self):
        """다른 사용자의 메모 삭제 시도 테스트"""
        self.client.login(username='otheruser', password='otherpassword123')
        response = self.client.get(reverse('memo_delete', args=[self.memo.pk]))
        self.assertEqual(response.status_code, 404)


class TestUrlPatterns(TestCase):
    """URL 라우팅 테스트"""
    
    def test_signup_url(self):
        """회원가입 URL 테스트"""
        url = reverse('signup')
        self.assertEqual(url, '/signup/')
    
    def test_memo_list_url(self):
        """메모 목록 URL 테스트"""
        url = reverse('memo_list')
        self.assertEqual(url, '/')
    
    def test_memo_detail_url(self):
        """메모 상세 URL 테스트"""
        url = reverse('memo_detail', args=[1])
        self.assertEqual(url, '/memo/1/')
    
    def test_memo_create_url(self):
        """메모 생성 URL 테스트"""
        url = reverse('memo_create')
        self.assertEqual(url, '/memo/create/')
    
    def test_memo_update_url(self):
        """메모 수정 URL 테스트"""
        url = reverse('memo_update', args=[1])
        self.assertEqual(url, '/memo/1/edit/')
    
    def test_memo_delete_url(self):
        """메모 삭제 URL 테스트"""
        url = reverse('memo_delete', args=[1])
        self.assertEqual(url, '/memo/1/delete/')


class TestIntegrationWorkflows(TestCase):
    """통합 워크플로우 테스트"""
    
    def test_complete_memo_workflow(self):
        """완전한 메모 워크플로우 테스트 (생성 -> 조회 -> 수정 -> 삭제)"""
        # 1. 사용자 생성 및 로그인
        user = User.objects.create_user(
            username='workflowuser',
            email='workflow@example.com',
            password='workflowpassword123'
        )
        self.client.login(username='workflowuser', password='workflowpassword123')
        
        # 2. 메모 생성
        create_response = self.client.post(reverse('memo_create'), {
            'title': '워크플로우 테스트',
            'content': '워크플로우 테스트 내용'
        })
        self.assertEqual(create_response.status_code, 302)
        memo = Memo.objects.get(title='워크플로우 테스트')
        
        # 3. 메모 목록에서 확인
        list_response = self.client.get(reverse('memo_list'))
        self.assertEqual(list_response.status_code, 200)
        self.assertContains(list_response, '워크플로우 테스트')
        
        # 4. 메모 상세 조회
        detail_response = self.client.get(reverse('memo_detail', args=[memo.pk]))
        self.assertEqual(detail_response.status_code, 200)
        self.assertContains(detail_response, '워크플로우 테스트 내용')
        
        # 5. 메모 수정
        update_response = self.client.post(reverse('memo_update', args=[memo.pk]), {
            'title': '수정된 워크플로우 테스트',
            'content': '수정된 워크플로우 테스트 내용'
        })
        self.assertEqual(update_response.status_code, 302)
        
        # 6. 수정된 내용 확인
        updated_memo = Memo.objects.get(pk=memo.pk)
        self.assertEqual(updated_memo.title, '수정된 워크플로우 테스트')
        
        # 7. 메모 삭제
        delete_response = self.client.post(reverse('memo_delete', args=[memo.pk]))
        self.assertEqual(delete_response.status_code, 302)
        self.assertFalse(Memo.objects.filter(pk=memo.pk).exists())
    
    def test_user_isolation_workflow(self):
        """사용자 간 데이터 격리 워크플로우 테스트"""
        # 두 사용자 생성
        user1 = User.objects.create_user('user1', 'user1@example.com', 'password123')
        user2 = User.objects.create_user('user2', 'user2@example.com', 'password123')
        
        # 사용자1로 로그인하여 메모 생성
        self.client.login(username='user1', password='password123')
        self.client.post(reverse('memo_create'), {
            'title': '사용자1 메모',
            'content': '사용자1 메모 내용'
        })
        
        # 사용자2로 로그인하여 메모 생성
        self.client.login(username='user2', password='password123')
        self.client.post(reverse('memo_create'), {
            'title': '사용자2 메모',
            'content': '사용자2 메모 내용'
        })
        
        # 사용자2는 자신의 메모만 볼 수 있음
        response = self.client.get(reverse('memo_list'))
        self.assertContains(response, '사용자2 메모')
        self.assertNotContains(response, '사용자1 메모')
        
        # 사용자1의 메모에 접근할 수 없음
        user1_memo = Memo.objects.get(title='사용자1 메모')
        response = self.client.get(reverse('memo_detail', args=[user1_memo.pk]))
        self.assertEqual(response.status_code, 404)
