<template>
  <n-card
    :title="`issue#${row.number}:  ${row.title}`"
    closable
    @close="handleClose"
    style="height: 100%; padding: 20px"
  >
    <svg ref="treemap" style="width：100% "></svg>
    <footer>
      <n-button @click="treeBack" attr-type="reset" style="padding-bottom: 5px">
        back
      </n-button>
    </footer>
  </n-card>
  <!-- <div style="height: 100%; padding: 20px">
    
  </div> -->
</template>

<script>
import * as d3 from "d3";
import { uid } from "../utils/uid.js";
import { inject, ref, onMounted, forceUpdate } from "vue";
export default {
  name: "TreeMap",
  props: {
    row: {
      type: Object,
    },
    height: {
      type: Number,
      default: 580,
    },
    dataAll: {
      type: Object,
    },
  },
  data() {
    const owner = inject("owner");
    const repo = inject("repo");
    return {
      uid: 0,
      owner,
      repo,
      pulls: this.dataAll.pulls,
      data: {},
      subData: {},
      parent: {},
      path: [],
      depth: 0,
      recalculate: false,
    };
  },

  mounted() {
    this.data = this.pulls[this.row.id].files;
    this.subData = JSON.parse(JSON.stringify(this.data));
    this.drawTree(this.height);
  },
  watch: {
    height() {
      // this.recalculate = true;
      this.drawTree(this.height);
    },
    row() {
      this.data = this.pulls[this.row.id].files;
      this.subData = JSON.parse(JSON.stringify(this.data));
      this.drawTree(this.height);
    },
  },
  methods: {
    handleClose() {
      this.$emit("callBackClose", this.row.id);
      // d3.select(this.$refs.treemap).selectAll("*").remove();
    },
    treeBack() {
      this.subData = this.parent;
      this.depth--;
      this.parent = JSON.parse(JSON.stringify(this.data));
      for (let i = 0; i < this.path.length; i++) {
        for (let j = 0; j < this.parent.children.length; j++) {
          if (this.parent.children[j].name == this.path[i]) {
            this.parent = this.parent.children[j];
            break;
          }
        }
      }
      this.path.pop();
      this.drawTree(this.height);
    },
    drawTree(height) {
      d3.select(this.$refs.treemap).selectAll("*").remove();
      // const color = d3.scaleSequential([10, 0], d3.interpolateCool);
      const color = d3.scaleSequential([0, 1.2], d3.interpolateBlues);
      // const color1 = d3.rgb(204, 255, 255);
      // const color2 = d3.rgb(0, 229, 230);
      // const color = d3.scaleSequential([12, 0], d3.interpolateRgb(color1, color2));
      // d3.interpolatePurples;
      // d3.interpolateGnBu;

      const format = d3.format(",d");
      const width = 570; //954
      // const height = 580; //1060

      let treemap = (data) =>
        d3
          .treemap()
          .size([width, height])
          .paddingOuter(7)
          .paddingTop(19)
          .paddingInner(4)
          .tile(d3.treemapSquarify)
          .round(false)(
          d3
            .hierarchy(data)
            .sum((d) => (!d.children ? d.addition + d.deletion : 0))
            .sort((a, b) => b.height - a.height)
        );

      const root = treemap(this.subData);
      // const nodes = root.descendants();
      console.log(this.recalculate, this.subData);
      const svg = d3
        .select(this.$refs.treemap)
        .append("svg")
        .attr("preserveAspectRatio", "xMidYMid meet")
        .attr("viewBox", [0, 0, width, height])
        .style("font", "10px sans-serif");

      const shadow = uid("shadow");

      svg
        .append("filter")
        .attr("id", shadow.id)
        .append("feDropShadow")
        .attr("flood-opacity", 0)
        .attr("dx", 0)
        .attr("stdDeviation", 3);

      const node = svg
        .selectAll("g")
        .data(d3.group(root, (d) => d.height))
        .join("g")
        .attr("filter", shadow)
        .selectAll("g")
        .data((d) => d[1])
        .join("g")
        .attr("transform", (d) => `translate(${d.x0},${d.y0})`);
      // the title is the tooltip that appears when you hover over a node
      node.append("title").text(
        (d) =>
          `${d
            .ancestors()
            .reverse()
            .map((d) => d.data.name)
            .join("/")}\n${format(d.value)}`
      );
      // the rect is the actual rectangle that represents the node
      console.log("root value", root.value);
      node
        .append("rect")
        .attr("id", (d) => (d.nodeUid = uid("node")).id)
        // .attr("fill", (d) => color(d.height))
        .attr("fill", (d) =>
          d.children || root.value == 0 ? "white" : color(d.value / root.value)
        )
        .attr("width", (d) => d.x1 - d.x0)
        .attr("height", (d) => d.y1 - d.y0)
        .attr("stroke", "black") // Set the border color to black
        .attr("stroke-width", 0.5); // Set the border width to 1 pixel

      // the clipPath is the part of the rectangle that is visible
      node
        .append("clipPath")
        .attr("id", (d) => (d.clipUid = uid("clip")).id)
        .append("use")
        .attr("xlink:href", (d) => d.nodeUid.href);

      // can only excute one time
      if (!this.recalculate) {
        node.each((d) => {
          // console.log(d);
          d.data.addition = d.copy().sum((d1) => (d1.children ? 0 : d1.addition)).value;
          d.data.deletion = d.copy().sum((d1) => (d1.children ? 0 : d1.deletion)).value;
          this.recalculate = false;
        });
      } // the text is the text that is displayed inside the node
      node
        .append("text")
        .attr("clip-path", (d) => d.clipUid)
        .selectAll("tspan")
        .data((d) =>
          d.data.name
            .split(/(=[A-Z][^A-Z])/g)
            .concat(
              "add: " + format(d.data.addition) + " ",
              "del: " + format(d.data.deletion)
            )
        )
        .join("tspan")
        .attr("fill-opacity", (d, i, nodes) =>
          i === nodes.length - 1 || i === nodes.length - 2 ? 0.7 : null
        )
        .text((d) => d);

      node
        .filter((d) => d.children)
        .selectAll("tspan")
        .attr("dx", 3) //margin of text from left side of node
        .attr("y", 13);

      node
        .filter((d) => !d.children)
        .selectAll("tspan")
        .attr("x", 3)
        .attr(
          "y",
          (d, i, nodes) => `${(i === nodes.length - 1) * 0.3 + 1.1 + i * 0.9}em`
        );
      console.log("---------------------", node);
      svg.selectAll("rect").on("click", (event, d) => {
        console.log("click-------------", event, "/////", d);
        d3.select(this.$refs.treemap).selectAll("*").remove();
        // let path = [];

        let tmp = [];
        while (d.parent) {
          tmp.push(d.data.name);
          d = d.parent;
        }
        if (this.depth == 0) {
          this.path = [];
          tmp.push(d.data.name);
        }

        this.path = this.path.concat(tmp.reverse());
        this.subData = JSON.parse(JSON.stringify(this.data));
        for (let i = 0; i < this.path.length; i++) {
          this.depth++;
          for (let j = 0; j < this.subData.children.length; j++) {
            if (this.subData.children[j].name == this.path[i]) {
              this.parent = this.subData;
              this.subData = this.subData.children[j];
              break;
            }
          }
        }

        this.drawTree(this.height);
      });
    },
  },
};
</script>

<style>
.treemap {
  width: 100%;
  height: 100%;
}

svg {
  width: 100%;
  height: 100%;
  font: 10px sans-serif;
}
</style>
