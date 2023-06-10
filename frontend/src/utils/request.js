import axios from "axios";

export async function fetchData(type, owner, repo) {
    try {
        const response = await axios.post(`http://localhost:5000/fetch_data`, {
          type: type,
          owner: owner,
          repo: repo,
        });
        return response.data;
      } catch (error) {
        console.error(error);
      }
}