import { query } from "./driver.js";

export async function billsByCarrier(carrier) {
  return query("SELECT * FROM bills WHERE carrier = '" + carrier + "'");
}
