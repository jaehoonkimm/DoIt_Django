from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.


class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        # 포스트 목록 페이지 가져오기
        response = self.client.get('/blog/')
        # 정상적인 페이지 로드
        self.assertEqual(response.status_code, 200)
        # 페이지 타이틀 => Blog
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')
        # 네브바 있음
        navbar = soup.nav
        # 네브바에 Blog, About Me 문구?
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        # 포스트가 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)
        # Main 구역에 게시물이 없다는 표시 표출
        main_area = soup.find('div', id='main-area')
        self.assertIn("아직 게시물이 없습니다", main_area.text)

        # 포스트가 2개 있다면 ..
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content="Hello world. We are the world.",
        )

        post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content="나는 두번째",
        )
        self.assertEqual(Post.objects.count(), 2)
