import Head from "next/head";
import { Text, Code, Note, Input, ButtonGroup, Button } from "@geist-ui/react";
import Center from "react-center";
import useSWR from "swr";
export default function Home(props) {
  console.log(props);
  const fetcher = (...args) => fetch(...args).then((res) => res.json());
  let initialData = props;
  const { data, error } = useSWR(`/api/${props.id}/main`, fetcher, {
    initialData,
    refreshInterval: 1000,
  });
  console.log
  async function Cancel() {
    let res = await fetch(
      `https://99bac19acf0e.ngrok.io/ticket-delete?ticket_id=${props.id}`
    ).then((r) => r.text());
    console.log(res);
  }
  return (
    <div>
      <Head>
        <title>Manage Ticker | Carrier Piegon</title>
      </Head>
      <Center style={{ height: "100vh" }}>
        <main
          style={{ padding: "12px 12px", width: "100vh", textAlign: "center" }}
        >
          <Text h2 style={{ fontSize: "2.0em" }}>
            Ticket <Code>{data.id}</Code>
          </Text>
          <Note label={false}>
            <Text
              h1
              style={{
                fontSize: "24em",
                marginBlockStart: "-0.3em",
                marginBlockEnd: "-0.25em",
              }}
            >
              {data.number}
            </Text>
          </Note>
          {data.number == "X" ? (
            <Button
              style={{ width: "100%", marginTop: "1em" }}
              type="error"
              ghost
              disabled
              onClick={() => Cancel()}
            >
              This Ticker No Longer Exists
            </Button>
          ) : (
            <Button
              style={{ width: "100%", marginTop: "1em" }}
              type="error"
              ghost
              onClick={() => Cancel()}
            >
              Cancel
            </Button>
          )}
        </main>
      </Center>
    </div>
  );
}

export async function getServerSideProps(context) {
  let { fetchData } = require("./api/[id]/main");
  return await { props: (await fetchData(context.params.id)) };
}
