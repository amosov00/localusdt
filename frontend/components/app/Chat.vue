<template lang="pug">
  div.chat
    h2 Отправьте сообщение
      =' '
      span.orange {{ name }}
    Textarea(v-model="textArea" class="w-100 mt-20"
      placeholder="Напишите трейдеру сообщение с контактной или другой информацией (необязательно)"
      @keydown.enter.native="sendMessage" ref="chatText")
    Button(green @click.native="sendMessage").mt-20.mr-15 Отправить
    span(v-if="chatConnected") Подключено
    span(v-else) Не подключено
    main.chat__box
      div(v-if="chatMessages.length <= 0").mt-20.mb-15.text-center.chat__empty Чат пока пуст!
      PerfectScrollbar(:options="{ wheelPropagation: false, minScrollbarLength: 32 }" ref="chatScroll")
        div.chat__content
          div.chat__message(v-for="msg in chatMessages")
            div {{ msg.message_body }}
            div {{ timestampToUtc(msg.created_at) }}
</template>

<script>
import { PerfectScrollbar } from "vue2-perfect-scrollbar";
import Textarea from '~/components/app/Textarea'
import Button from '~/components/app/Button'
import formatDate from "~/mixins/formatDate";

export default {
  mixins: [formatDate],
  props: ['name','invoice'],
  components: {
    PerfectScrollbar,
    Textarea,
    Button
  },
  data: () => ({
    chatMessages: [],
    chatConnected: false,
    textArea: '',
    ws: null,
    audio: null
  }),
  methods: {
    playSound() {
      if(this.audio instanceof Audio) {
        this.audio.pause()
        this.audio.currentTime = 0;
        this.audio.play()
      } else {
        this.audio = new Audio(require('~/assets/sounds/soft_notification.mp3'));
        this.audio.play()
      }
    },
    sendMessage(e) {
      if (e.shiftKey) {
        return
      }
      e.preventDefault()
      this.ws.send(this.textArea)
      this.textArea = ''
    },
    chatConnect() {
      let token = this.$cookies.get('token')
      this.ws = new WebSocket(`wss://localusdt-dev.elastoo.com/api/invoice/ws/${this.invoice.chat_id}?token=${token}`);
      this.ws.onopen = (e) => {
        this.chatConnected = true;
      }
      this.ws.onerror = (e) => {
        this.chatConnected = false;
      }
      this.ws.onmessage = (e) => {
        this.playSound();
        this.chatMessages.push(JSON.parse(e.data))
        let container = this.$refs.chatScroll.$el;
        let scrollAtEnd = container.scrollHeight - container.scrollTop === container.clientHeight;
        if(scrollAtEnd) {
          this.$nextTick(() => {
            container.scrollTo({ top: container.scrollHeight, left: 0, behavior: 'smooth'})
          })
        }
      }
    }
  },
  async mounted() {
    let messages = await this.$store.dispatch('invoice/getChatroomMessages', this.invoice.chat_id);
    this.chatMessages = messages;

    let container = this.$refs.chatScroll.$el;
    let scrollAtEnd = container.scrollHeight - container.scrollTop === container.clientHeight;
    if(scrollAtEnd) {
      this.$nextTick(() => {
        container.scrollTo(0, container.scrollHeight)
      })
    }
    this.chatConnect()
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
  &__content {
    padding-right: 10px;
  }

  &__empty {
    color: #7f828b;
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
      height: 64px;
      background: linear-gradient(to bottom, #dddddd, rgba(0, 0, 0, 0)
      );
      top: 0;
      left: 0;
      position: absolute;
      pointer-events: none;
      opacity: 0.2;
    }
  }

  &__message {
    display: block;
    border: 1px solid $grey;
    border-radius: 6px 6px 6px 0px;
    padding: 20px;
    margin: 10px;
    font-style: italic;
    font-size: 14px;
    color: $grey-dark;
    max-width: 200px;
    width: 100%;

    &:nth-child(odd) {
      margin-left: auto;
      background-color: $grey;
      border-radius: 6px 6px 0px 6px;
    }
  }
}
</style>
