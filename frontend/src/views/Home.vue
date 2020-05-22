<template>
  <v-data-table
    :headers="headers"
    :items="data"
    class="elevation-1"
    hide-default-footer
  >
    <template v-slot:top>
      <v-toolbar flat color="white">
        <v-toolbar-title>Feed</v-toolbar-title>
        <v-divider
          class="mx-4"
          inset
          vertical
        ></v-divider>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on }">
            <v-btn color="primary" dark class="mb-2" v-on="on">Add New Source</v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" sm="6" md="4">
                    <v-text-field v-model="editedItem.title" label="Title"></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="8">
                    <v-text-field v-model="editedItem.url" label="URL"></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="save">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon
        small
        class="mr-2"
        @click="editItem(item)"
      >
        mdi-pencil
      </v-icon>
      <v-icon
        small
        class="mr-2"
        @click="fetchItem(item)"
      >
        mdi-refresh
      </v-icon>
      <v-icon
        small
        class="mr-2"
        @click="deleteItem(item)"
      >
        mdi-delete
      </v-icon>
    </template>
    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize">Reset</v-btn>
    </template>
  </v-data-table>
</template>

<script>
import FeedService from '../services/feed.service';

  export default {
    data: () => ({
      dialog: false,
      headers: [
        { text: 'Title', value: 'title' },
        { text: 'URL', value: 'url' },
        { text: 'Create Date', value: 'create_date' },
        { text: 'Last Fetch', value: 'last_fetch' },
        { text: 'Last Updated', value: 'last_updated' },
        { text: 'Terminated', value: 'terminated' },

        { text: 'Actions', value: 'actions', sortable: false },
      ],
      data: [],
      editedIndex: -1,
      editedItem: {
        title: '',
        url: '',
      },
      defaultItem: {
        title: '',
        url: '',
      },
    }),
    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
      },
    },
    watch: {
      dialog (val) {
        val || this.close()
      },
    },
    created () {
      this.initialize()
    },
    methods: {
      initialize () {
        FeedService.getFeed().then(
          response => {
            this.data = response.data.results;
          },
          error => {
            this.data =
              (error.response && error.response.data) ||
              error.message ||
              error.toString();
          }
          )
      },
      editItem (item) {
        this.editedIndex = this.data.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },
      deleteItem (item) {
        const index = this.data.indexOf(item)
        if (confirm('Are you sure you want to delete this item?')) {
          {
            FeedService.deleteFeed(item).then(
              response => {
                this.initialize()
              },
              error => {
                this.data =
                  (error.response && error.response.data) ||
                  error.message ||
                  error.toString();
              }
              )
          }
        }
      },
      fetchItem (item) {
            FeedService.fetchFeed(item).then(
              response => {
                this.initialize()
              },
              error => {
                this.data =
                  (error.response && error.response.data) ||
                  error.message ||
                  error.toString();
              }
              )
          },
      close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },
      save () {
        if (this.editedIndex > -1) {
          FeedService.updateFeed(this.editedItem).then(
          response => {
            this.initialize()
          },
          error => {
            this.data =
              (error.response && error.response.data) ||
              error.message ||
              error.toString();
          }
          )
        } else {
          FeedService.addFeed(this.editedItem.title, this.editedItem.url).then(
          response => {
            this.data.push(response.data)
          },
          error => {
            this.data =
              (error.response && error.response.data) ||
              error.message ||
              error.toString();
          }
          )
        }
        this.close()
      },
    },
  }
</script>