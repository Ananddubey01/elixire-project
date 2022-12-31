<template>
  <div class="container">
  <form>
    <label for="queryType">Enter type of search</label>
    <select
      class="col-2 form-select w-100"
      id="queryType"
      v-model="searchParams.queryType"
    >
      <option value="" disabled>-Please Select the type of query-</option>
      <option value="amazonsingle">Amazon Product Page Query</option>
      <option value="amazonquery">Amazon Search Page Query</option>
      <option value="tata1mgquery">tata 1mg Search Page Query</option>
      <option value="tata1mgsingle">tata 1mg Product Page Query</option>
    </select>
    <input
      class="form-control mt-2"
      id="url"
      placeholder="Enter Url"
      v-model="searchParams.url"
    />
    <button
      type="submit"
      class="btn btn-primary"
      @click.prevent="filterParams(searchParams)"
    >
      Get Data
    </button>
  </form>
</div>
</template>
<script setup>
import { ref, defineEmits } from "vue";
const emit = defineEmits(["searchParams"]);
const searchParams = ref({
  url:"",
  queryType:""
});
function filterParams(searchParams) {
  if(searchParams.queryType=="")
    alert("please enter valid search type")
  else if(searchParams.url=="")
    alert("please enter the url")
  else
    emit("searchParams", searchParams);
}
</script>
<style scoped></style>
