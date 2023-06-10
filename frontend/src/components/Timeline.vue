<template>
  <n-card
    title="Timeline"
    style="height: 100%"
    content-style="padding-left:18px; padding-right:18px;padding: 0"
    foot-style="padding: 0;"
    borderd="true"
  >
    <div ref="timeline"></div>
  </n-card>
</template>

<script>
import * as d3 from "d3";
// import { toRaw } from "@vue/reactivity";
// import axios from "axios";
import starData from "../assets/data/modelmapper_modelmapper_stars.json";
import forkData from "../assets/data/modelmapper_modelmapper_forks.json";
import pullData from "../assets/data/modelmapper_modelmapper_pulls.json";
// import { fetchData } from "../utils/.request.js";
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Timeline",
  props: {
    myProp: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      starData: [],
      forkData: [],
      pullData: [],
    };
  },
  mounted() {
    this.drawTimeline();
  },
  methods: {
    async drawTimeline() {
      //-----------get data
      // this.starData = await fetchData("star", this.myProp.owner, this.myProp.repo);
      // this.forkData = await fetchData("fork", this.myProp.owner, this.myProp.repo);
      this.starData = starData;
      this.forkData = forkData;
      this.pullData = pullData;
      this.starData.splice(0, 1); // the first element is {total_stars:2109}
      this.forkData.splice(0, 1);

      // Parse date format 2010-11-30T17:06:24Z
      const parseDate = d3.utcParse("%Y-%m-%dT%H:%M:%S%Z");
      console.log("starData", this.starData);
      this.starData = this.starData.map((d) => ({
        date: parseDate(d.starredAt),
        value: 1,
        type: "star",
        name: d.name,
      }));

      this.forkData = this.forkData.map((d) => ({
        date: parseDate(d.createdAt),
        value: 1,
        type: "fork",
      }));
      this.pullData = this.pullData.map((d) => ({
        date: parseDate(d.createdAt),
        value: 1,
        type: "pullRequest",
        title: d.title,
      }));
      const data = [...this.starData, ...this.forkData, ...this.pullData];
      // Create SVG element
      const margin = { top: 30, right: 30, bottom: 0, left: 50 };
      const width = 1560 - margin.left - margin.right; //1260
      const height = 250 - margin.top - margin.bottom; //500

      const svg = d3
        .select(this.$refs.timeline)
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      // Create x-axis and y-axis scales
      const x = d3
        .scaleUtc()
        .domain(d3.extent(data, (d) => d.date))
        .range([0, width]);

      const y = d3
        .scaleLinear()
        .range([height, 0])
        .domain([
          0,
          d3.max(data, (d) =>
            d3.sum(
              data.filter((di) => di.date <= d.date),
              (d) => d.value
            )
          ),
        ]);

      // Create x-axis and y-axis
      const xAxis = d3.axisBottom(x);

      const yAxis = d3.axisLeft(y).tickFormat((d) => d);

      // Append x-axis and y-axis
      svg
        .append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

      svg.append("g").call(yAxis);

      // Add fork points to the chart
      svg
        .selectAll(".point")
        .data(data)
        .enter()
        .append("circle")
        .attr("class", "point1")
        .attr("cx", (d) => x(d.date))
        .attr("cy", (d) =>
          y(
            d3.sum(
              data.filter((di) => (di.date <= d.date) & (di.type == "fork")),
              (d) => d.value
            )
          )
        )
        .attr("r", 3)
        .style("fill", "#1f77b4");

      // Add star points to the chart
      // star points may have bugs，because the mouseover interaction will show d.name is undefined and the datetime is frpm fork
      svg
        .selectAll(".point")
        .data(data)
        .enter()
        .append("circle")
        .attr("class", "point2")
        .attr("cx", (d) => x(d.date))
        .attr("cy", (d) =>
          y(
            d3.sum(
              data.filter((di) => (di.date <= d.date) & (di.type == "star")),
              (d) => d.value
            )
          )
        )
        .attr("r", 3)
        .style("fill", "#ffb6c1");

      // Add pr points to the chart
      svg
        .selectAll(".point")
        .data(data)
        .enter()
        .append("circle")
        .attr("class", "point3")
        .attr("cx", (d) => x(d.date))
        .attr("cy", (d) =>
          y(
            d3.sum(
              data.filter((di) => (di.date <= d.date) & (di.type == "pullRequest")),
              (d) => d.value
            )
          )
        )
        .attr("r", 3)
        .style("fill", "	#B0E0E6");

      // Add title
      svg
        .append("text")
        .attr("class", "title")
        .attr("x", width / 2)
        .attr("y", 0 - margin.top / 2)
        .attr("text-anchor", "middle")
        .text("Star/Fork Timeline");
      // Add x-axis label
      svg
        .append("text")
        .attr(
          "transform",
          "translate(" + width / 2 + " ," + (height + margin.top + 20) + ")"
        )
        .style("text-anchor", "middle")
        .text("Time");

      // Add y-axis label
      svg
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - height / 2)
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Total Count");

      // Add legend
      const legend = svg
        .selectAll(".legend")
        .data([
          ["Star", "#FFB6C1"],
          ["Fork", "#1f77b4"],
          ["Pull Request", "	#B0E0E6"],
        ])
        .enter()
        .append("g")
        .attr("class", "legend")
        .attr("transform", function (d, i) {
          return "translate(" + (width - 100) + "," + (i * 20 + 10) + ")";
        });

      legend
        .append("circle")
        .attr("cx", 5)
        .attr("cy", 5)
        .attr("r", 5)
        .style("fill", function (d) {
          return d[1];
        });

      legend
        .append("text")
        .attr("x", 20)
        .attr("y", 5)
        .attr("dy", ".35em")
        .style("text-anchor", "start")
        .text(function (d) {
          return d[0];
        });

      // Add mouseover interaction to show name and date
      svg
        .selectAll(".point2")
        .on("mouseover", function (event, d) {
          console.log(d.name);
          console.log(typeof d.name);
          console.log(d.date);
          d3.select(this).transition().duration("50").attr("r", 6);
          const name = d.name == null ? "anonym" : d.name;
          svg
            .append("text")
            .attr("class", "name")
            .attr("x", x(d.date))
            .attr("y", y(d.value) + 10)
            .text(`${name} \n ${d.date.toLocaleDateString()}`);
        })
        .on("mouseout", function () {
          d3.select(this).transition().duration("50").attr("r", 3);
          svg.selectAll(".name").remove();
        });
      //fork points mouseover
      svg
        .selectAll(".point1")
        .on("mouseover", function (event, d) {
          d3.select(this).transition().duration("50").attr("r", 6);
          svg
            .append("text")
            .attr("class", "name")
            .attr("x", x(d.date))
            .attr("y", y(d.value) + 10)
            .text(`${d.date.toLocaleDateString()}`);
        })
        .on("mouseout", function () {
          d3.select(this).transition().duration("50").attr("r", 3);
          svg.selectAll(".name").remove();
        });

      //pr points mouseover
      svg
        .selectAll(".point3")
        .on("mouseover", function (event, d) {
          d3.select(this).transition().duration("50").attr("r", 6);
          svg
            .append("text")
            .attr("class", "name")
            .attr("x", x(d.date))
            .attr("y", y(d.value) + 10)
            .text(`${d.title}${d.date.toLocaleDateString()}`);
        })
        .on("mouseout", function () {
          d3.select(this).transition().duration("50").attr("r", 3);
          svg.selectAll(".name").remove();
        });
    },
  },
};
</script>

<style scoped>
.area {
  fill: none;
}
.legend circle {
  stroke-width: 2px;
  stroke: #69b3a2;
}
.legend text {
  font-size: 14px;
  font-weight: bold;
}
</style>
