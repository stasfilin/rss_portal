<template>
    <v-container fluid>
        <v-data-iterator
                :items="items"
                :page="page"
                hide-default-footer
        >
            <template v-slot:default="props">
                <v-row>
                    <v-col
                            v-for="item in props.items"
                            :key="item.title"
                            cols="12"
                            sm="6"
                            md="4"
                            lg="6"
                    >
                        <v-card
                                class="mx-auto"
                                max-width="800"
                        >
                            <v-card-actions>
                                <v-btn icon v-if="item.is_read" disabled>
                                    <div>
                                        <v-icon color="grey">mdi-check</v-icon>
                                    </div>
                                </v-btn>
                                <v-spacer></v-spacer>
                                <v-btn icon>
                                    <div v-if="item.is_favorite">
                                        <v-icon color="red" @click="addFavourite(item)">mdi-heart</v-icon>
                                    </div>
                                    <div v-else>
                                        <v-icon @click="addFavourite(item)">mdi-heart</v-icon>
                                    </div>
                                </v-btn>
                            </v-card-actions>
                            <v-card-text>
                                <p class="display-1 text--primary">
                                    <a v-bind:href="item.link" target="_blank" @click="changeToRead(item)">{{ item.title }}</a>
                                </p>
                                <p>{{ item.author }}</p>
                                <div class="text--primary">
                                    <p v-html="item.summary"></p>
                                </div>
                            </v-card-text>
                            <v-expand-transition>
                                <v-timeline dense clipped>
                                    <v-timeline-item
                                            fill-dot
                                            class="white--text mb-1"
                                            color="blue"
                                            large
                                    >
                                        <v-text-field
                                                v-model="input"
                                                hide-details
                                                flat
                                                label="Leave a comment..."
                                                solo
                                                @keydown.enter="addComment(item)"
                                        >
                                            <template v-slot:append>
                                                <v-btn
                                                        class="mx-0"
                                                        depressed
                                                        @click="addComment(item)"
                                                >
                                                    Post
                                                </v-btn>
                                            </template>
                                        </v-text-field>
                                    </v-timeline-item>

                                    <v-timeline-item
                                            v-for="event in item.comments"
                                            class="mb-4"
                                            color="blue"
                                            small
                                    >
                                        <v-row justify="space-between">
                                            <v-col cols="7" v-text="event.content"></v-col>
                                            <v-col cols="5" class="text-right">
                                                <v-btn icon>
                                                    <div>
                                                        <v-icon color="grey" @click="removeComment(event)">mdi-delete</v-icon>
                                                    </div>
                                                </v-btn>
                                            </v-col>
                                        </v-row>
                                        <v-row justify="space-between">
                                            <v-col cols="7" v-text="event.date_added"></v-col>
                                        </v-row>
                                    </v-timeline-item>
                                </v-timeline>
                            </v-expand-transition>
                        </v-card>
                    </v-col>
                </v-row>
            </template>

            <template v-slot:footer>
                <v-row class="mt-2" align="center" justify="center">
                    <v-btn @click="loadMore()">More</v-btn>
                </v-row>
            </template>
        </v-data-iterator>
    </v-container>
</template>

<script>
    import FeedService from '../services/feed.service';
    import CommentService from '../services/comment.service'

    export default {
        data() {
            return {
                search: '',
                filter: {},
                page: 1,
                offset: 10,
                itemsPerPage: 10,
                show: false,
                keys: [
                    'title',
                    'link',
                    'summary',
                    'author',
                    'comments',
                    'published',
                    'is_favorite',
                    'is_read',

                ],
                items: [],
            }
        },
        created() {
            this.initialize()
        },
        methods: {
            initialize() {
                FeedService.getFeedItems().then(
                    response => {
                        this.items = response.data.results;
                    },
                    error => {
                        this.data =
                            (error.response && error.response.data) ||
                            error.message ||
                            error.toString();
                    }
                )
            },
            addFavourite: function (article) {
                FeedService.makeFavourite(article.id).then(
                    response => {
                        this.initialize();
                    },
                    error => {
                        this.data =
                            (error.response && error.response.data) ||
                            error.message ||
                            error.toString();
                    }
                );
            },
            addComment: function (article) {
                if (this.input) {
                    CommentService.addComment(article, this.input).then(
                        response => {
                            article.comments.unshift(response.data)
                            this.input = '';
                        },
                        error => {
                            this.data =
                                (error.response && error.response.data) ||
                                error.message ||
                                error.toString();
                        }
                    );
                } else {
                    alert('Fields Empty');
                }
            },

            changeToRead: function (article) {
                FeedService.makeRead(article.id).then(
                    response => {
                        this.initialize();
                    },
                    error => {
                        this.data =
                            (error.response && error.response.data) ||
                            error.message ||
                            error.toString();
                    }
                );
            },

            removeComment: function (comment) {
                CommentService.deleteComment(comment).then(
                    response => {
                        this.initialize();
                    },
                    error => {
                        this.data =
                            (error.response && error.response.data) ||
                            error.message ||
                            error.toString();
                    }
                );
            },
            loadMore() {
                this.page += 1
                this.offset += this.itemsPerPage
                FeedService.getFeedItems(this.offset).then(
                    response => {
                        this.items = response.data.results
                    },
                    error => {
                        this.data =
                            (error.response && error.response.data) ||
                            error.message ||
                            error.toString();
                    }
                )
            }
        },
    }
</script>