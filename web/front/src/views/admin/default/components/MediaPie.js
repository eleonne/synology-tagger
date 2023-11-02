// Chakra imports
import { Box, Flex, Text, Select, useColorModeValue } from "@chakra-ui/react";
// Custom components
import Card from "components/card/Card.js";
import PieChart from "components/charts/PieChart";
import { VSeparator } from "components/separator/Separator";
import {getPieChartOptions} from '../../../../assets/utils'
import { pieChartData, pieChartOptions } from "variables/charts";
import axios from "axios";
import React, { useEffect, useState } from "react";
import ReactApexChart from "react-apexcharts";

export default function MyPie(props) {
  const { ...rest } = props;

  const [state, setState] = useState({
    'labels': null,
    'values': null,
    'total': 0
  })

  useEffect(() => {
    axios.get(process.env.REACT_APP_BASE_URL + '/api/get-video-trend-split?column=' + props.column).then((response) => {
      const res = {
        'labels': getPieChartOptions(response.data.data.labels, props.formatter),
        'values': response.data.data.values,
        'total': response.data.data.total
      }
      setState({...res})
    })
  }, []);

  // Chakra Color Mode
  const textColor = useColorModeValue("secondaryGray.900", "white");
  const total = (props.formatter) ? props.formatter(state.total) : state.total.toLocaleString('pt-BR')
  return (
    <Card p='20px' align='center' direction='column' w='100%' {...rest}>
      <Flex
        px={{ base: "0px", "2xl": "10px" }}
        justifyContent='space-between'
        alignItems='center'
        w='100%'
        mb='8px'>
        <Text color={textColor} fontSize='md' fontWeight='600' mt='4px'>
          {props.title}: {total}
        </Text>
      </Flex>
      <Flex w='100%' flexDirection={{ base: "column", lg: "row" }}>
        <Box minH='260px' minW='85%' mt='auto'>
          {
            (state.values === null) ? null :
            <ReactApexChart
                options={state.labels}
                series={state.values}
                type='pie'
                width='100%'
                height='100%'
              />
          }
        </Box>
      </Flex>
    </Card>
  );
}
