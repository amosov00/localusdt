<template lang="pug">
    div.chat
        h2 {{ $t('chat.sendMessage') }}
        =' '
        span(v-if="!adminChat").orange {{ name }}
        Textarea( v-if="!adminChat" v-model="textArea" class="w-100 mt-20"
            :placeholder="$t('chat.placeholder')"
            @keydown.enter.native="sendMessage" ref="chatText")
        Button( v-if="!adminChat" green @click.native="sendMessage").mt-20.mr-15 {{ $t('chat.send') }}
        main.chat__box
            div(v-if="chatMessages.length <= 0").mt-20.mb-15.text-center.chat__empty {{ $t('chat.empty') }}
            PerfectScrollbar(
            :options="{ wheelPropagation: false, minScrollbarLength: 32 }"
            ref="chatScroll")
                div.chat__content(ref="chatsContent")
                    div.chat__message(
                    v-for="(msg, i) in chatMessages"
                    :key="i"
                    :class="{'chat__message--me' : msg.sender === user.username }")
                        div.chat__message-header
                            span.chat__username {{ msg.sender }}
                            span.chat__date  {{ formatDate(msg.created_at) }}
                            div.chat__message-body {{ msg.message_body }}
</template>

<script>
import { PerfectScrollbar } from "vue2-perfect-scrollbar";
import Textarea from '~/components/app/Textarea'
import Button from '~/components/app/Button'
import formatDate from "~/mixins/formatDate";
import VueNativeSock from 'vue-native-websocket'
import Vue from 'vue'
Vue.use(VueNativeSock, `${process.env.API_WS_URL}`, {
connectManually: true,
reconnectionAttempts: 5, // (Number) number of reconnection attempts before giving up (Infinity),
reconnectionDelay: 3000,
})
export default {
mixins: [formatDate],
props: ['name','invoice','adminChat'],
components: {
    PerfectScrollbar,
    Textarea,
    Button
},
data: () => ({
    chatMessages: [],
    textArea: '',
    ws: null,
    audio: null,
    socketPing: null,
    connect: true

}),
computed: {
    user() {
    return this.$store.getters.user;
    }
},
watch:{
    chatMessages(){
    setTimeout(() => {
        let container = this.$refs.chatScroll.$el;
        container.scrollTop = container.scrollHeight
    });
    }
},
methods: {
    playSound(filename) {
    if(this.audio instanceof Audio) {
        this.audio.pause()
        this.audio.currentTime = 0;
    }

    this.audio = new Audio(require(`~/assets/sounds/${filename}`));
    this.audio.play()
    },
    sendMessage(e) {
        if(this.textArea.length <= 0 ) {
            if(e.code === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            }
            return
        }
        if (e.shiftKey) {
            return
        }

        let cleanedMsg = this.textArea.trim();
        e.preventDefault()

        if(cleanedMsg.length > 0) {
            setTimeout(() => {
            let container = this.$refs.chatScroll.$el;
            container.scrollTop = container.scrollHeight
            });
            this.$socket.send(cleanedMsg)
        }
        this.textArea = ''
    },
    chatConnect() {
    //let token = this.$cookies.get('token');
        this.$connect(`${process.env.API_WS_URL}invoice/ws/${this.invoice.chat_id}/`, { format: 'json' })
        this.connect = false

    this.$socket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        if(this.user.username !== data.sender) {
            this.playSound('soft_notification.mp3');
        } else {
            this.playSound('message-sent.mp3');
        }
        this.chatMessages.push(data)
        if(this.$refs.chatScroll){
        let container = this.$refs.chatScroll.$el;
        let scrollAtEnd = container.scrollHeight - container.scrollTop === container.clientHeight;
        if(scrollAtEnd) {
            this.$nextTick(() => {
            let chatContent = document.querySelector('.chat__content');
            // chatContent.lastChild.scrollIntoView();
            chatContent.scrollTop = 1000000
            })
        }
        }
    }
    }
},
async mounted() {
  if(this.adminChat){
    let res = await this.$axios.get(`/admin/users/chat/${this.$route.params.id}/`)
    this.chatMessages = res.data.messages
    return
  }
    let messages = await this.$store.dispatch('invoice/getChatroomMessages', this.invoice.chat_id);
    this.chatMessages = messages;
    let container;
    if(this.$refs.chatScroll){
      container = this.$refs.chatScroll.$el;
      let scrollAtEnd = container.scrollTop - container.scrollHeight
      this.$nextTick(() => {
          container.scrollTop = container.scrollHeight
      })
      if(this.connect){
          this.chatConnect()
      }
    }

}
}
</script>

<style lang="scss">
.ps {
.ps__rail-y {
    opacity: 0.6;
}
}

.chat {
flex: 1 1 0;
margin-right: 93px;
&__content {
    padding: 20px;
}

&__empty {
    color: #7f828b;
}

&__message-header {
    font-size: 12px;
    margin-bottom: 5px;
}

&__date {
    color: #888B8E;
}

&__username {
    color: #11171D;
    font-weight: 500;
    display: inline-block;
    margin-right: 3px;
}

&__box {
    margin-top: 20px;
    border-top: 1px solid $grey;
    height: 300px;
    display: flex;
    flex-direction: column;
    align-content: center;
    position: relative;
    &:after {
    content: "";
    width: 100%;
    height: 30px;
    background: linear-gradient(to bottom, #dddddd, rgba(0, 0, 0, 0));
    top: 0;
    left: 0;
    position: absolute;
    pointer-events: none;
    opacity: 0.2;
    }
}

&__message {
    text-align: left;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 20px;

    &:last-child {
    margin-bottom: 0;
    }

    &--me {
    align-items: flex-end;

    .chat__message-body {
        border: 1px solid #E5F4EF;
        background: rgba(72, 177, 144, 0.05);
        border-radius: 6px 6px 0 6px;
        text-align: right;
    }
    }
}

&__message-body {
    border: 1px solid #CFD1D2;
    padding: 10px;
    border-radius: 6px 6px 6px 0;
    font-size: 14px;
    line-height: 170%;
    color: #11171D;
    max-width: 300px;
    min-width: 161px;
    text-align: left;
}
}
</style>
