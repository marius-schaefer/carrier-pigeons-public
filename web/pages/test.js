import Head from "next/head";
import { Text, Code, Note, Input, ButtonGroup, Button } from "@geist-ui/react";
import Center from "react-center";

export default function Home(props) {
  console.log(props)
  return (
    <div>
      <Head>
        <title>Manage Ticker | Carrier Piegon</title>
      </Head>
      <Center style={{ height: '100vh'}}>
        <main style={{ padding: "12px 12px", width: '100vh', textAlign: "center" }}>
          <Text h2 style={{ fontSize: '2.0em'}}>
            Ticket <Code>10342-3</Code>
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
              {props.number}
            </Text>
          </Note>

          <Button
            style={{ width: "100%", marginTop: "1em" }}
            type="error"
            ghost
            onClick={() => window.close()}
          >
            Cancel
          </Button>
        </main>
      </Center>
    </div>
  );
}

export async function getStaticProps(context) {
  console.log('hi!')
  return {
    props: {number: 7},
  }
}