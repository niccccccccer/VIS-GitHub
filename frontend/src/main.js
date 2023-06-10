import { createApp,reactive } from 'vue'
import App from './App.vue'
import naive from 'naive-ui'

const app = createApp(App);
const globalVars = reactive({
    owner: 'soot-oss',
    repo: 'soot'
  })
  
app.provide('globalVars', globalVars)
app.use(naive).mount('#app');
