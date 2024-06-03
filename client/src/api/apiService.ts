import axios from "axios";
import Response from "./responseType";

/**
 * Asynchronous function that sends a POST request to a specified endpoint with a given body.
 *
 * @param endpoint The endpoint to send the POST request to.
 * @param body The body of the POST request containing a 'code' property.
 * @returns An object containing the response data and any error that occurred during the request.
 */
export default async function postRequest(
  endpoint: string,
  body: { code: string }
) {
  let data: string = "";
  let error: string = "";
  const baseURL: string = import.meta.env.VITE_SERVER_BASE_URL;
  const url: string = `${baseURL}${endpoint}`;
  try {
    const response: Response = await axios({
      method: "post",
      url: url,
      data: body,
    });
    data = response.data;
  } catch (err) {
    error = err;
  }
  return { data, error };
}
