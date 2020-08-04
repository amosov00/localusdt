<template>
  <div class="checkbox">
    <label class="check option">
      <input class="check__input" type="checkbox" />
      <svg class="check__box" viewBox="0 0 25 25">
        <rect class="check__focus" width="20" height="20" rx="4" />
        <rect class="check__square" x="3" y="3" width="14" height="14" rx="2" />
        <polyline class="check__mark" points="5 9 9 13 15 6" />
      </svg>
      {{label}}
    </label>
  </div>
</template>

<script>
export default {
  props: {
    label: String
  }
}
</script>

<style lang="scss">
.checkbox {
  margin-bottom: 40px;
  font-style: italic;
  font-size: 14px;
  display: flex;
  align-items: center;
  cursor: pointer !important;
}
.option {
  display: block;
  margin-bottom: 0.5em;
}
.check {
  padding-left: 1.2em;
}

.check__input {
  position: absolute;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  
}

.check__box {
  position: absolute;
  margin-left: -1.2em;
  width: 1em;
  height: 1em;
}

.check__focus {
  fill: none;
}

.check__square {
  fill: #ffffff;
  stroke: #48B190;
  stroke-width: 2px;
}

.check__mark {
  fill: none;
  stroke: #ffffff;
  stroke-width: 3px;
}

/* Checked */

.check__input:checked + * .check__square {
  fill: #48B190;
}

/* Disabled */

.check__input:disabled + * .check__square {
  stroke: #9b9b9b;
}

.check__input:checked:disabled + * .check__square {
  fill: #9b9b9b;
}
</style>
