<template>
  <n-card
    title="Timeline"
    style="height: 100%"
    :header-style="{
      fontsize: '16px',
      background: 'rgba(250, 250, 252, 1)',
      padding: '8px 8px 8px 16px',
    }"
    content-style="padding-left:18px; padding-right:18px;padding-bottom: 0;"
    borderd="true"
  >
    <div ref="timeline" style="height: 100%"></div>
  </n-card>
</template>

<script>
import * as d3 from "d3";
import { inject } from "vue";
// import { fetchData } from "../utils/.request.js";
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Timeline",
  props: {
    dataAll: {
      type: Object,
    },
  },

  data() {
    const repo = inject("repo");
    return {
      repo,
      starData: this.dataAll.stars,
      forkData: this.dataAll.forks,
      pulls: this.dataAll.pulls,
    };
  },
  mounted() {
    this.drawTimeline();
  },
  watch: {
    repo() {
      console.log("repo change in timeline", this.dataAll);
      this.starData = this.dataAll.stars;
      this.forkData = this.dataAll.forks;
      this.pulls = this.dataAll.pulls;
      this.drawTimeline();
    },
  },
  methods: {
    drawTimeline() {
      d3.select(this.$refs.timeline).selectAll("*").remove();
      const colors = {
        star: "#ffb6c1",
        fork: "#1f77b4",
        pr: "#B0E0E6",
        highlight: "#006400",
      };

      // Parse date format 2010-11-30T17:06:24Z
      const parseDate = d3.utcParse("%Y-%m-%dT%H:%M:%S%Z");
      this.starData = this.starData.map((d) => ({
        date: parseDate(d.starredAt),
        value: d.value,
        type: "star",
        name: d.name,
      }));

      this.forkData = this.forkData.map((d) => ({
        date: parseDate(d.createdAt),
        value: d.value,
        type: "fork",
      }));
      this.pulls = this.pulls.map((d) => ({
        date: parseDate(d.createdAt),
        value: d.value,
        type: "pullRequest",
        title: d.title,
        id: d.value - 1,
        number: d.number,
      }));
      const data = [...this.starData, ...this.forkData, ...this.pulls];
      // Create SVG element
      const margin = { top: 30, right: 30, bottom: 0, left: 50 };
      const width = 1860 - margin.left - margin.right; //1260
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
      const length = [this.starData.length, this.forkData.length, this.pulls.length];
      const y = d3
        .scaleLinear()
        .range([height, 0])
        .domain([0, d3.max(length, (d) => d)]);

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
        .data(data.filter((di) => di.type == "fork"))
        .enter()
        .append("circle")
        .attr("class", "point1")
        .attr("cx", (d) => x(d.date))
        .attr("cy", (d) => y(d.value))
        .attr("r", 3)
        .style("fill", colors.fork);

      // Add star points to the chart
      // star points may have bugs，because the mouseover interaction will show d.name is undefined and the datetime is frpm fork
      svg
        .selectAll(".point")
        .data(data.filter((di) => di.type == "star"))
        .enter()
        .append("circle")
        .attr("class", "point2")
        .attr("cx", (d) => x(d.date))
        .attr("cy", (d) => y(d.value))
        .attr("r", 3)
        .style("fill", colors.star);

      // Add pr points to the chart
      svg
        .selectAll(".point")
        .data(data.filter((di) => di.type == "pullRequest"))
        .enter()
        .append("circle")
        .attr("class", "point3")
        .attr("cx", (d) => x(d.date))
        .attr("cy", (d) => y(d.value))
        .attr("r", 3)
        .style("fill", colors.pr);

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
          ["Star", colors.star],
          ["Fork", colors.fork],
          ["Pull Request", colors.pr],
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

      // Add star points mouseover interaction to show name and date
      svg
        .selectAll(".point2")
        .on("mouseover", function (event, d) {
          console.log(d.name, typeof d.name, d.date);
          d3.select(this)
            .transition()
            .duration("50")
            .attr("r", 6)
            .style("fill", colors.highlight);
          const name = d.name == null ? "anonym" : d.name;
          svg
            .append("text")
            .attr("class", "name")
            .attr("x", x(d.date))
            .attr("y", y(d.value + 100))
            .text(`${name} \n ${d.date.toLocaleDateString()}`);
        })
        .on("mouseout", function () {
          d3.select(this)
            .transition()
            .duration("50")
            .attr("r", 3)
            .style("fill", colors.star);
          svg.selectAll(".name").remove();
        });
      //fork points mouseover
      svg
        .selectAll(".point1")
        .on("mouseover", function (event, d) {
          d3.select(this)
            .transition()
            .duration("50")
            .attr("r", 6)
            .style("fill", colors.highlight);
          svg
            .append("text")
            .attr("class", "name")
            .attr("x", x(d.date))
            .attr("y", y(d.value + 100))
            .text(`${d.date.toLocaleDateString()}`);
        })
        .on("mouseout", function () {
          d3.select(this)
            .transition()
            .duration("50")
            .attr("r", 3)
            .style("fill", colors.fork);
          svg.selectAll(".name").remove();
        });

      //pr points mouseover
      svg
        .selectAll(".point3")
        .on("mouseover", function (event, d) {
          d3.select(this)
            .transition()
            .duration("50")
            .attr("r", 6)
            .style("fill", colors.highlight);

          svg
            .append("text")
            .attr("class", "name")
            .attr("x", x(d.date))
            .attr("y", y(d.value + 100))
            .text(`${d.title}${d.date.toLocaleDateString()}`);
        })
        .on("mouseout", function () {
          d3.select(this)
            .transition()
            .duration("50")
            .attr("r", 3)
            .style("fill", colors.pr);
          svg.selectAll(".name").remove();
        })
        .on("click", (event, d) => {
          // console.log("click-------------", event, "/////", d);
          this.$emit("callBackPointSelect", d);
          // d3.select(this).attr("fill", "rgb(0,100,0)");
        });

      // --------------添加折线
      var line = d3
        .line()
        .x(function (d) {
          return x(d.date);
        })
        .y(function (d) {
          return y(d.value);
        })
        .curve(d3.curveCatmullRom); //这里有多种形态可以选择
      const lineWidth = "2";
      svg
        .append("path")
        .attr("class", "line1")
        .attr(
          "d",
          line(
            data.filter((di) => di.type == "star"),
            (d) => x(d.date),
            (d) => y(d.value)
          )
        )
        .attr("stroke", colors.star)
        .attr("stroke-width", lineWidth)
        .attr("fill", "none");

      svg
        .append("path")
        .attr("class", "line2")
        .attr(
          "d",
          line(
            data.filter((di) => di.type == "fork"),
            (d) => x(d.date),
            (d) => y(d.value)
          )
        )
        .attr("stroke", colors.fork)
        .attr("stroke-width", lineWidth)
        .attr("fill", "none");

      svg
        .append("path")
        .attr("class", "line3")
        .attr(
          "d",
          line(
            data.filter((di) => di.type == "pullRequest"),
            (d) => x(d.date),
            (d) => y(d.value)
          )
        )
        .attr("stroke", colors.pr)
        .attr("stroke-width", lineWidth)
        .attr("fill", "none");

      //   let transform = d3.zoomIdentity;
      //   let points = svg.selectAll("circle");
      //   const zoom = d3.zoom().on("zoom", (e) => {
      //     svg.attr("transform", (transform = e.transform));
      //     svg.style("stroke-width", 3 / Math.sqrt(transform.k));
      //     points.attr("r", 3 / Math.sqrt(transform.k));
      //   });

      //   return svg.call(zoom).call(zoom.transform, d3.zoomIdentity);
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
