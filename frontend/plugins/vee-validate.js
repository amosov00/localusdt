import { extend, localize } from 'vee-validate'
import {
  required,
  email,
  min,
  confirmed,
  max,
  regex,
  alpha_num,
  alpha,
  alpha_spaces,
  min_value
} from 'vee-validate/dist/rules'
import en from 'vee-validate/dist/locale/en.json'

localize({
  en
})

extend('email', {
  ...email,
  message: 'Не валидная почта'
})
extend('min', {
  ...min,
  message: 'Пароль должен быть больше или равен 8 символам'
})
extend('userName', {
  message: `Ваше имя пользователя не соответствует нашему стандарту имён пользователей, убедитесь что:<br>
  — Ваше имя больше 6 и меньше 20 символов. <br>
  — Ваше имя не содержит нижние подчеркивания — ни в начале, ни в конце. <br>
  — Ваше имя не содержит спец. символов. <br>
  — Ваше имя состоит только из латинских символов. <br>`,
  validate: value => value.match(/^(?=[a-zA-Z0-9._]{6,20}$)(?!.*[_.]{2})[^_.].*[^_.]$/) !== null
})
extend('max', max)
extend('regex', regex)
extend('alpha', alpha)
extend('alpha_num', alpha_num)
extend('alpha_spaces', alpha_spaces)
extend('required', {
  ...required,
  message: 'Это поле обязательно'
})
extend('confirmed', {
  ...confirmed,
  message: 'Пароли не совпадают'
})
extend('upCase', {
  message: "Пароль должен содержать минимум один заглавный символ",
  validate: value => value.match(/[A-Z]/g) !== null
})
extend('lowCase', {
  message: "Пароль должен содержать минимум один строчный символ",
  validate: value => value.match(/[a-z]/g) !== null
})
extend('number', {
  message: "Пароль должен содержать минимум одину цифру",
  validate: value => value.match(/[0-9]/g) !== null
})

extend('pwd', {
  message: `Ваш пароль не соответствует нашему стандарту паролей, убедитесь что:<br>
    — Ваш пароль больше 8 символов. <br>
    — Ваш пароль содержит минимум один заглавный и строчный символы. <br>
    — Ваш пароль содержит минимум одину цифру. <br>
    — Ваш пароль не содержит спец. символов. <br>
    — Ваш пароль состоит только из латинских символов. <br>`,
  validate: value => value.match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/) !== null
})