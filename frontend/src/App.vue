<template>
  <div class="container" style="height: calc(100vh)">
    <n-grid :cols="26" style="height: 25%">
      <n-gi span="5">
        <BasicIntro v-if="isShow" :dataAll="dataAll" />
      </n-gi>
      <n-gi span="21">
        <Timeline
          v-if="isShow"
          :dataAll="dataAll"
          style="padding-left: 50px"
          @callBackPointSelect="handleInfo"
        />
      </n-gi>
    </n-grid>
    <n-grid :cols="26" style="height: 75%">
      <n-gi span="6">
        <PullRequest
          v-if="isShow"
          @callBackInfo="handleInfo"
          @callBackBrush="handleBrush"
        />
      </n-gi>
      <n-gi span="20">
        <n-grid :cols="2" style="height: 100%">
          <n-gi v-for="(item, index) in infos" :key="index"
            ><Formtree
              v-if="isShow"
              :dataAll="dataAll"
              @callBackClose="handleClose"
              :row="item"
              :height="calHeight"
            ></Formtree>
          </n-gi>
        </n-grid>
      </n-gi>
    </n-grid>
  </div>
</template>

<script>
// import HelloWorld from "./components/HelloWorld.vue";
import Timeline from "./components/Timeline3.vue";
import PullRequest from "./components/PullRequest.vue";
import BasicIntro from "./components/BasicIntro.vue";
import Formtree from "./components/Formtree3.vue";
import { NGrid, NGridItem } from "naive-ui";
import { ref, provide, reactive } from "vue";
import axios from "axios";
export default {
  name: "App",
  components: {
    // HelloWorld,
    Timeline,
    PullRequest,
    Formtree,
    BasicIntro,
  },

  data() {
    let owner = ref("modelmapper");
    provide("owner", owner);
    let repo = ref("modelmapper");
    provide("repo", repo);
    const calHeight = 580;
    return {
      owner,
      repo,
      infos: [],
      indexes: [],
      length: 0,
      isShow: false,
      calHeight,
      dataAll: {},
    };
  },
  created() {
    // let data = ref(null);
    // provide("dataAll", data);
    console.log("requets", this.owner, this.repo);
    axios
      .post(`http://localhost:5000/fetch_data`, {
        owner: this.owner,
        repo: this.repo,
      })
      .then((response) => {
        this.dataAll = response.data;
        this.isShow = true;
      })
      .catch((error) => {
        console.error(error);
      });
  },

  watch: {
    repo() {
      this.isShow = false;
      console.log("Repo changes", this.repo);
      axios
        .post(`http://localhost:5000/fetch_data`, {
          type: "pull",
          owner: this.owner,
          repo: this.repo,
        })
        .then((response) => {
          this.dataAll = response.data;
          this.isShow = true;
          console.log(response.data);
          this.infos = [];
          this.indexes = [];
          this.length = 0;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  methods: {
    handleInfo(data) {
      if (data.id != -1 && this.indexes.indexOf(data.id) === -1) {
        this.indexes.push(data.id);
        this.infos.push(data);
        this.length++;
        this.calHeight = 640 / Math.floor((this.length + 1) / 2);
        console.log(
          "I get the value from pull request component",
          this.infos,
          this.length,
          this.calHeight
        );
      }
    },
    handleBrush(data) {
      data.forEach((item) => {
        this.handleInfo(item);
      });
    },
    handleClose(data) {
      this.length--;
      this.calHeight = 640 / Math.floor((this.length + 1) / 2);
      console.log("I get the close value from formtree component", data, this.indexes);
      for (let i = 0; i < this.indexes.length; i++) {
        console.log(this.indexes[i], data);
        if (this.indexes[i] == data) {
          this.indexes.splice(i, 1);
          this.infos.splice(i, 1);
          console.log("the close data is", i, this.indexes, this.infos);

          break;
        }
      }
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 5px;
}

.container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.timeline {
  width: 100%;
  height: 100%;
}

.formtree {
  width: 100%;
  height: 100%;
}
</style>
