// Next.js API route support: https://nextjs.org/docs/api-routes/introduction

export const fetchData = async (id) => {
  var axios = require("axios");
  var data = JSON.stringify({ ticket_id: id });
  try {
    var config = {
      method: "post",
      url: "https://99bac19acf0e.ngrok.io/ticket-actions",
      headers: {
        "Content-Type": "application/json",
      },
      data: data,
    };

    let res = await axios(config)
      .then(function (response) {
        return response.data;
      })
      .catch(function (error) {
        console.log(error);
      });
    console.log(res);
    console.log(typeof res);
    return {
      number: typeof res == "number" ? res : "X",
      id: id,
    };
  } catch {
    return {
      number: "X",
      id: id,
    };
  }
};

export default async (req, res) => {
  res.send(await fetchData(req.query.id))
}