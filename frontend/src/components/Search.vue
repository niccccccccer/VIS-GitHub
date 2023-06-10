<template>
  <div>
    <div id="visualization"></div>
  </div>
</template>

<script>
import * as d3 from "d3";
import elasticlunr from "elasticlunr";
import modelData from "../assets/data/modelmapper_modelmapper.json";

export default {
  name: "SemanticSearch",
  mounted() {
    this.search();
  },
  data() {
    return {
      searchTerm: "",
      searchResults: [],
    };
  },
  methods: {
    search() {
      const index = elasticlunr(function () {
        this.addField("title");
        this.addField("body");
        this.setRef("number");
      });

      modelData.forEach(function (doc) {
        index.addDoc(doc);
      });

      const results = index.search(this.searchTerm, {
        fields: {
          title: { boost: 2 },
          body: { boost: 1 },
        },
      });

      this.searchResults = results.map(function (result) {
        return modelData.find(function (doc) {
          return doc.number === parseInt(result.ref);
        });
      });
      console.log("---------------");
      console.log(this.searchResults);
      // D3 scatter plot
      d3.select("#visualization")
        .selectAll("div")
        .data(this.searchResults)
        .join("div")
        .style("background-color", "steelblue")
        .style("color", "white")
        .style("padding", "10px")
        .style("margin", "5px")
        .style("width", "300px")
        .text(function (d) {
          return d.title;
        });
    },
  },
};
</script>
