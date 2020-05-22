import axios from 'axios';
import authHeader from './auth-header';

const API_URL = 'http://localhost:8000/api/';

class CommentService {
  addComment(article, content) {
    return axios.post(API_URL + 'comment/', {
        feed_item_id: article.id,
        content: content
      },
        { headers: authHeader() });
  }

  deleteComment(comment) {
    return axios.delete(API_URL + 'comment/'+comment.id, { headers: authHeader() });
  }
}

export default new CommentService();
