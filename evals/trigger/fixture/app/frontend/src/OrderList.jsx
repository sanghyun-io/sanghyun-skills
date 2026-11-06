import { useEffect, useState } from "react";
import { api } from "./api";
export default function OrderList() {
  const [data, setData] = useState();
  useEffect(() => { api.get("/orders").then((r) => setData(r.data)); }, []);
  return <ul>{data.orders.map((o) => <li key={o.id}>{o.total}</li>)}</ul>;
}
