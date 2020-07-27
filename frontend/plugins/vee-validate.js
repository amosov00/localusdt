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
  message: 'This field must be a valid email'
})
extend('min', {
  ...min,
  message: 'Password must be greater than or equal to 8 characters'
})
extend('max', max)
extend('regex', regex)
extend('alpha', alpha)
extend('alpha_num', alpha_num)
extend('alpha_spaces', alpha_spaces)
extend('required', {
  ...required,
  message: 'This field is required'
})
extend('confirmed', {
  ...confirmed,
  message: 'Password does not match'
})
extend('min_value', {
  ...min_value,
  message: 'Value must be greater than or equal to 500 characters'
})
