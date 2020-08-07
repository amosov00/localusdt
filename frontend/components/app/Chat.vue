<template>
  <div class="chat">
    <h2>Отправьте сообщение <span class="orange">USERuser1234</span></h2>
    <Textarea
      class="w-100 mt-20"
      placeholder="Напишите трейдеру сообщение с контактной или другой информацией 
(необязательно)"
    />
    <Button green class="mt-20">Отправить</Button>

    <main class="chat__box">
      <p class="chat__message">Hello!</p>
      <p class="chat__message">Hello!</p>
      <p class="chat__message">Hello!</p>
      <p class="chat__message">Hello!</p>
      <p class="chat__message">Hello!</p>
      <p class="chat__message">Hello!</p>
      <p class="chat__message">Hello!</p>
      <p class="chat__message">Hello!</p>
      <p class="chat__message">Hello!</p>
      <p class="chat__message">Hello!</p>
      <p class="chat__message">Hello!</p>
      <p class="chat__message">Hello!</p>
      <p class="chat__message">Hello!</p>
      <p class="chat__message">Hello!</p>
    </main>
  </div>
</template>

<script>
import Textarea from '~/components/app/Textarea'
import Button from '~/components/app/Button'
export default {
  components: {
    Textarea,
    Button
  }
}
</script>

<style lang="scss">
.chat {

  &__box {
    margin-top: 20px;
    border-top: 1px solid $grey;
    height: 300px;
    overflow-y: scroll;
    display: flex;
    flex-direction: column;
    align-content: center;
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
