function displayBlogPosts(type = 'recent') {
  const filename = type === 'recent' ? 'recent_blog_posts.json' : 'recommended_blog_posts.json';
  
  fetch(`data/${filename}`)
      .then(response => response.json())
      .then(data => {
          const blogList = document.getElementById('blog-posts');
          blogList.innerHTML = '';
          
          data.articles.forEach(article => {
              blogList.innerHTML += `
                  <a href="${article.url}" class="bg-white p-6 rounded-lg shadow-md hover:bg-wood-medium hover:text-white transition-colors">
                      <h3 class="text-lg font-bold text-wood-dark mb-2">${article.title}</h3>
                      <div class="text-gray-700 line-clamp-3">
                          ${article.content}
                      </div>
                  </a>
              `;
          });
      })
      .catch(error => {
          console.error('Error loading blog posts:', error);
      });
}

function setupTabs() {
  const recommendedTab = document.getElementById('recommended-tab');
  const recentTab = document.getElementById('recent-tab');

  const setActiveTab = (activeTab, inactiveTab) => {
      activeTab.classList.add('border-wood-dark', 'text-wood-dark');
      activeTab.classList.remove('border-transparent', 'text-gray-500');
      
      inactiveTab.classList.remove('border-wood-dark', 'text-wood-dark');
      inactiveTab.classList.add('border-transparent', 'text-gray-500');
  };

  recommendedTab.addEventListener('click', () => {
      setActiveTab(recommendedTab, recentTab);
      displayBlogPosts('recommended');
  });

  recentTab.addEventListener('click', () => {
      setActiveTab(recentTab, recommendedTab);
      displayBlogPosts('recent');
  });
}

document.addEventListener('DOMContentLoaded', () => {
  setupTabs();
  displayBlogPosts('recent'); // デフォルトで最新を表示
});