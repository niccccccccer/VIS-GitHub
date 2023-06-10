<template>
  <div class="treemap" ref="treemap"></div>
</template>

<script>
import * as d3 from "d3";
// import { toRaw } from "@vue/reactivity";
import data from "../assets/data/modelmapper_modelmapper_tree_format.json";
// import data from "../assets/data/flare-2.json";
import { uid } from "../utils/uid.js";
import { fetchData } from "@/utils/request";
export default {
  name: "TreeMap",
  props: {
    myProp: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      data: [],
      // width: 954,
      // height: 1060,
      // format: d3.format(",d"),
      // color: d3.scaleSequential([8, 0], d3.interpolateMagma),
      uid: 0,
    };
  },
  mounted() {
    console.log(data);
    this.drawTree();
  },
  methods: {
    async drawTree() {
      this.data = data;
      // this.data = await fetchData("tree", this.myProp.owner, this.myProp.repo);
      console.log("-----------------");
      console.log(this.data);
      const color = d3.scaleSequential([10, 0], d3.interpolateCool);
      const format = d3.format(",d");
      // const height = 1060;
      // const width = 954;
      const width = 800;
      const height = 1600;
      // let ratio = 1;
      let treemap = (data) =>
        d3
          .treemap()
          .size([width, height])
          .paddingOuter(7)
          .paddingTop(19)
          .paddingInner(4)
          .tile(d3.treemapResquarify.ratio(1))
          .round(true)(
          d3
            .hierarchy(data)
            .sum((d) => d.value)
            .sort((a, b) => b.height - a.height || b.value - a.value)
        );

      const root = treemap(this.data);
      // const nodes = root.descendants();
      // console.log(nodes);

      const svg = d3
        .select(this.$refs.treemap)
        .append("svg")
        .attr("viewBox", [0, 0, width, height])
        .style("font", "10px sans-serif");

      const shadow = uid("shadow");
      console.log(shadow);

      svg
        .append("filter")
        .attr("id", shadow.id)
        .append("feDropShadow")
        .attr("flood-opacity", 0.3)
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
      node
        .append("rect")
        .attr("id", (d) => (d.nodeUid = uid("node")).id)
        .attr("fill", (d) => color(d.height))
        .attr("width", (d) => d.x1 - d.x0)
        .attr("height", (d) => d.y1 - d.y0);
      // the clipPath is the part of the rectangle that is visible
      node
        .append("clipPath")
        .attr("id", (d) => (d.clipUid = uid("clip")).id)
        .append("use")
        .attr("xlink:href", (d) => d.nodeUid.href);
      // the text is the text that is displayed inside the node
      node
        .append("text")
        .attr("clip-path", (d) => d.clipUid)
        .selectAll("tspan")
        .data((d) => d.data.name.split(/(=[A-Z][^A-Z])/g).concat(format(d.value)))
        .join("tspan")
        .attr("fill-opacity", (d, i, nodes) => (i === nodes.length - 1 ? 0.7 : null))
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

      return svg.node();
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
