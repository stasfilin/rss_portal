import Vue from 'vue';
import App from './App.vue';
import { router } from './router';
import store from './store';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import VeeValidate from 'vee-validate';
import Vuex from 'vuex';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
  faHome,
  faUser,
  faUserPlus,
  faSignInAlt,
  faSignOutAlt,
  faHeart
} from '@fortawesome/free-solid-svg-icons';

import 'element-ui/lib/theme-chalk/index.css'
import lang from 'element-ui/lib/locale/lang/en'
import locale from 'element-ui/lib/locale'
import VueMaterial from 'vue-material'

import vuetify from '@/plugins/vuetify'

library.add(faHome, faUser, faUserPlus, faSignInAlt, faSignOutAlt, faHeart);

Vue.config.productionTip = false;

Vue.use(VeeValidate);
Vue.use(VueMaterial);

Vue.component('font-awesome-icon', FontAwesomeIcon);

Vue.use(Vuex);
locale.use(lang)

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app');
