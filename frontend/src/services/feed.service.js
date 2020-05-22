import axios from 'axios';
import authHeader from './auth-header';

const API_URL = 'http://localhost:8000/api/';

class FeedService {
  getFeedItems(offset=10) {
    return axios.get(API_URL + 'feed-item/?offset='+offset, { headers: authHeader() });
  }

  makeFavourite(feed_item_id) {
    return axios.get(API_URL + 'feed-item/'+feed_item_id+'/favorite/', { headers: authHeader() });
  }

  getFeed() {
    return axios.get(API_URL + 'feed', { headers: authHeader() });
  }

  addFeed(title, url) {
    return axios.post(API_URL + 'feed/', {
        title: title,
        url: url
      },
        { headers: authHeader() });
  }

  updateFeed(data) {
    return axios.patch(API_URL + 'feed/'+data.id+'/', {
      title: data.title,
      url: data.url
        },
        { headers: authHeader() });
  }

  deleteFeed(data) {
    return axios.delete(API_URL + 'feed/'+data.id+'/',
        { headers: authHeader() });
  }

  fetchFeed(data) {
    return axios.get(API_URL + 'feed/'+data.id+'/fetch/',
        { headers: authHeader() });
  }

  makeRead(feed_item_id) {
    return axios.get(API_URL + 'feed-item/'+feed_item_id+'/read/', { headers: authHeader() });
  }
}

export default new FeedService();
