// Chakra imports
import {
    Box,
    Flex,
    Text,
    useColorModeValue,
  } from "@chakra-ui/react";
  // Custom components
  import Card from "components/card/Card.js";
  import LineChart from "components/charts/LineChart";
  import React, { useEffect, useState } from "react";
  import { getChartOptions, getChartData, secondsToDhms } from '../../../../assets/utils'
  import axios from "axios";
  
  export default function PhotoTrend(props) {
    const { ...rest } = props;
    const chartId = 'photos-trend-chart'
  
    const [state, setState] = useState({
      'labels': null,
      'values': null,
      'total': 0
    })
  
    useEffect(() => {
      axios.get(process.env.REACT_APP_BASE_URL + '/api/get-video-trend').then((response) => {
        const res = {
          'labels': getChartOptions(response.data.data.labels, chartId),
          'values': getChartData(response.data.data.values, "Tempo em segs"),
          'total': response.data.data.total
        }
        setState({...res})
      })
    }, []);
    
    const textColor = useColorModeValue("secondaryGray.900", "white");
    
    return (
      <Card
        justifyContent='center'
        align='center'
        direction='column'
        w='100%'
        mb='0px'
        {...rest}>
        <Flex justify='space-between' ps='0px' pe='20px' pt='5px'>
          <Flex align='center' w='100%'>
            <Text color={textColor}
              fontSize='34px'
              textAlign='start'
              fontWeight='700'
              lineHeight='100%'>
              Tempo total de vídeos: {secondsToDhms(state.total)}
            </Text>
          </Flex>
        </Flex>
        <Flex w='100%' flexDirection={{ base: "column", lg: "row" }}>
          <Box minH='260px' minW='85%' mt='auto'>
            {
              (state.values) ? 
                <LineChart
                  chartId={chartId}
                  chartData={state.values}
                  chartOptions={state.labels}
                /> : null
            }
          </Box>
        </Flex>
      </Card>
    );
  }
  