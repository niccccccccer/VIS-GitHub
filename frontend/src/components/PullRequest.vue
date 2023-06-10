<template>
  <n-card
    title="Pull Request"
    style="height: 100%"
    content-style="padding-left:18px; padding-right:18px;padding-bottom:0px"
    borderd="true"
    :header-style="{
      fontsize: '16px',
      background: 'rgba(250, 250, 252, 1)',
      padding: '8px 8px 8px 16px',
    }"
    :footer-style="{
      height: 0,
    }"
  >
    <n-grid :cols="1" style="height: 4%">
      <n-gi span="1">
        <n-form
          class="search-form"
          ref="formRef"
          :model="model"
          label-placement="left"
          label-width="auto"
          require-mark-placement="right-hanging"
          :style="{
            maxWidth: '640px',
          }"
        >
          <n-form-item>
            <n-input
              placeholder="query"
              v-model:value="model.query"
              type="text"
              path="query"
            >
              <template #suffix>
                <n-icon :component="FlashOutline" />
              </template>
            </n-input>
            <n-button attr-type="submit" @click="search" round> Go </n-button>
          </n-form-item>
        </n-form>
      </n-gi>
    </n-grid>
    <n-grid :cols="1" style="height: 45%">
      <n-gi span="1">
        <n-data-table
          :columns="columns"
          :data="results"
          :pagination="false"
          :bordered="false"
          striped
          :row-props="rowProps"
          :resizable="true"
          size="small"
      /></n-gi>
    </n-grid>
    <n-grid :cols="1" style="height: 50%">
      <n-gi span="1">
        <div ref="scatter" style="height: 100%"></div>
      </n-gi>
    </n-grid>
  </n-card>
</template>

<script>
import axios from "axios";
import { ref, inject } from "vue";
import * as d3 from "d3";
import { NButton, NGrid, NForm, NCard, NDataTable } from "naive-ui";

export default {
  data() {
    const owner = inject("owner");
    const repo = inject("repo");
    return {
      owner,
      repo,
      results: ref([]),
      scatterData: [],
      columns: [
        {
          title: "Number",
          key: "number",
          resizable: true,
          minWidth: 100,
        },
        {
          title: "Title",
          key: "title",
          // resizable: true,
        },
      ],
      formRef: ref(null),
      model: ref({ query: "" }),
      rowProps: (row) => {
        return {
          onClick: () => {
            console.log(1, row.id, row.number, row.title);
            const partInfo = row;
            this.$emit("callBackInfo", partInfo);
          },
        };
      },
    };
  },

  methods: {
    search() {
      console.log(1, this.model.query, this.owner, this.repo);
      axios
        .post(`http://localhost:5000/semantic_search`, {
          query: this.model.query,
          owner: this.owner,
          repo: this.repo,
        })
        .then((response) => {
          this.results = response.data;
        })
        .catch((error) => {
          console.error(error);
        });
      axios
        .post(`http://localhost:5000/dimensionality_reduction`, {
          query: this.model.query,
          owner: this.owner,
          repo: this.repo,
        })
        .then((response) => {
          this.scatterData = JSON.parse(response.data);

          this.drawScatter();
        })
        .catch((error) => {
          console.error(error);
        });
    },

    drawScatter() {
      const _this = this;

      const data = this.scatterData.map((d) => ({
        x: d.x,
        y: d.y,
        type: "normal",
        id: d.index,
        title: d.title,
        number: d.number,
      }));
      data[0].type = "query";
      console.log("drawwwwwwwwww", data.length, data[0]);

      const margin = { top: 10, right: 30, bottom: 10, left: 40 };
      const height = 900;
      const width = 1000;
      // create scales
      const x = d3
        .scaleLinear()
        .domain(d3.extent(data, (d) => d.x))
        .nice()
        .range([margin.left, width - margin.right]);
      const y = d3
        .scaleLinear()
        .domain(d3.extent(data, (d) => d.y))
        .nice()
        .range([height - margin.bottom, margin.top]);
      // create axes
      const xAxis = (g) =>
        g
          .attr("transform", `translate(0,${height - margin.bottom})`)
          .call(d3.axisBottom(x))
          .call((g) => g.select(".domain").remove())
          .call((g) =>
            g
              .append("text")
              .attr("x", width - margin.right)
              .attr("y", -4)
              .attr("fill", "#000")
              .attr("font-weight", "bold")
              .attr("text-anchor", "end")
              .text(data.x)
          );
      const yAxis = (g) =>
        g
          .attr("transform", `translate(${margin.left},0)`)
          .call(d3.axisLeft(y))
          .call((g) => g.select(".domain").remove())
          .call((g) =>
            g
              .select(".tick:last-of-type text")
              .clone()
              .attr("x", 4)
              .attr("text-anchor", "start")
              .attr("font-weight", "bold")
              .text(data.y)
          );
      d3.select(this.$refs.scatter).selectAll("*").remove();
      const svg = d3
        .select(this.$refs.scatter)
        .append("svg")
        .attr("viewBox", [0, 0, width, height])
        .property("value", []);

      const brush = d3.brush().on("start brush end", brushed);

      svg.append("g").call(xAxis);
      svg.append("g").call(yAxis);

      const dot1 = svg
        .append("g")
        .attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-width", 1.5)
        .selectAll("circle")
        .data(data.filter((d) => d.type == "normal"))
        .join("circle")
        .attr("transform", (d) => `translate(${x(d.x)},${y(d.y)})`)
        .attr("r", 3);
      const dot2 = svg
        .append("g")
        .attr("fill", "none")
        .attr("stroke", "red")
        .attr("stroke-width", 1.5)
        .selectAll("circle")
        .data(data.filter((d) => d.type == "query"))
        .join("circle")
        .attr("transform", (d) => `translate(${x(d.x)},${y(d.y)})`)
        .attr("r", 3);
      const dot = dot1.merge(dot2);
      svg.call(brush);

      function brushed({ selection }) {
        let value = [];
        if (selection) {
          const [[x0, y0], [x1, y1]] = selection;
          value = dot
            .style("stroke", "gray")
            .filter((d) => x0 <= x(d.x) && x(d.x) < x1 && y0 <= y(d.y) && y(d.y) < y1)
            .style("stroke", "steelblue")
            .append("title")
            .text("title")
            .data();
          _this.$emit("callBackBrush", value);
        } else {
          dot.style("stroke", "steelblue");
        }
        svg.property("value", value).dispatch("input");
      }

      return svg.node();
    },
  },
};
</script>

<style scoped>
/* lang="scss" */
/* .search-form {
  ::v-deep(.n-form-item .n-form-item-feedback-wrapper) {
    --n-feedback-height: 10px;
  }
} */
</style>
