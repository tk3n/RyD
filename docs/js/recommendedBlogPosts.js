function displayBlogPosts() {
  fetch('data/recommended_blog_posts.json')
    .then(response => response.json())
    .then(data => {
      const blogList = document.getElementById('recommended-blog-posts');
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

document.addEventListener('DOMContentLoaded', displayBlogPosts);
