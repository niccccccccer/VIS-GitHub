<template>
  <n-card
    title="Basic Introduction"
    style="height: 100%"
    :header-style="{
      fontsize: '16px',
      background: 'rgba(250, 250, 252, 1)',
      padding: '8px 8px 8px 16px',
    }"
    content-style="padding:15px;"
    borderd="true"
  >
    <n-grid :cols="1" style="height: 40%">
      <n-gi>
        <n-form
          ref="formRef"
          :model="model"
          label-placement="left"
          label-width="auto"
          require-mark-placement="right-hanging"
          label-align="left"
          :style="{
            maxWidth: '640px',
          }"
        >
          <n-form-item label="Select Owner" path="owner">
            <n-select
              v-model:value="model.owner"
              placeholder="Select"
              :options="owners"
            />
          </n-form-item>

          <n-form-item label="Select Repository" path="repo">
            <n-select v-model:value="model.repo" placeholder="Select" :options="repos" />
          </n-form-item>
        </n-form>
      </n-gi>
    </n-grid>
    <n-grid :cols="1" style="height: 40%; margin-top: 10px">
      <n-gi>
        <n-space vertical justify="center" align=" start">
          <!-- <n-tag>试一下有没有内容</n-tag> -->
          <n-tag size="large" style="margin-bottom: 20px">
            Description: {{ dataAll.description }}</n-tag
          >
          <n-tag>
            Link: <a :href="dataAll.homepageUrl">{{ dataAll.homepageUrl }}</a>
          </n-tag>
        </n-space>
      </n-gi>
    </n-grid>
    <n-space>
      <n-tag round :bordered="false">
        {{ dataAll.forkCount }} forks
        <template #avatar>
          <n-avatar
            src="https://cdnimg103.lizhi.fm/user/2017/02/04/2583325032200238082_160x160.jpg"
          />
        </template>
      </n-tag>
      <n-tag round :bordered="false">
        {{ dataAll.stargazerCount }} stars
        <template #avatar>
          <n-avatar
            src="https://cdnimg103.lizhi.fm/user/2017/02/04/2583325032200238082_160x160.jpg"
          />
        </template>
      </n-tag>

      <!-- <n-tag>
        320 forks
        <template #icon>
          <n-icon :component="Star16Regular" size="40" :depth="3"></n-icon>
        </template>
      </n-tag>

      <n-tag :bordered="false">
        2132 stars
        <template #icon>
          <n-icon :component="BranchFork16Regular" size="40" :depth="3"></n-icon>
        </template>
      </n-tag> -->
    </n-space>
  </n-card>
</template>

<script>
import { ref, inject, watch } from "vue";
// import { BranchFork16Regular, Star16Regular } from "@vicons/fluent";
export default {
  props: {
    dataAll: {
      type: Object,
    },
  },
  data() {
    const owner = inject("owner");
    const repo = inject("repo");
    // const dataAll = inject("dataAll");
    return {
      owners: ["soot-oss", "modelmapper", "vuejs", "scikit-learn"].map((v) => ({
        label: v,
        value: v,
      })),
      repos: ["soot", "modelmapper", "vue", "scikit-learn"].map((v) => ({
        label: v,
        value: v,
      })),
      formRef: ref(null),
      model: ref({ owner: owner, repo: repo, query: "" }),
    };
  },
  mounted() {},

  methods: {},
};
</script>

<style></style>
