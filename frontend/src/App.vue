<template>
  <v-app>
    <v-app-bar
      app
      color="white"
    >
      <v-toolbar-title to="/"><router-link to="/" class="nav-link">RSS Parser</router-link></v-toolbar-title>

      <div v-if="currentUser">
          <v-toolbar-title>
            <router-link to="/feed" class="nav-link">Feed Items</router-link>
          </v-toolbar-title>
      </div>

      <v-spacer></v-spacer>

      <div v-if="currentUser">
        <a href @click.prevent="logOut">
            Logout
        </a>
      </div>
      <div v-if="!currentUser">
        <router-link to="/login" class="nav-link">Login</router-link>
      </div>
      <div v-if="!currentUser">
        <router-link to="/register" class="nav-link">Register</router-link>
      </div>
    </v-app-bar>

    <v-content>
      <router-view/>
    </v-content>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
  }),
  computed: {
    currentUser() {
      return this.$store.state.auth.user;
    }
  },
  methods: {
    logOut() {
      this.$store.dispatch('auth/logout');
      this.$router.push('/login');
    }
  }
};
</script>
