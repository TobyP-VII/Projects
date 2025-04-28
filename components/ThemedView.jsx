import { SafeAreaView, View } from 'react-native'
import { Colors } from '../constants/colors'
import React from 'react'
import { useSafeAreaInsets } from 'react-native-safe-area-context'

const ThemedView = ({style, safe=false, ...props}) => {

    if (!safe) return (
        <View 
            style={[{
                flex: 1,
                alignItems: 'center',
                justifyContent: 'center',
                backgroundColor: Colors.background,
            },
            style
            ]}
            {...props}
        />
    )

    const insets = useSafeAreaInsets()

    return (
        <View 
            style={[{
                flex: 1,
                alignItems: 'center',
                justifyContent: 'center',
                backgroundColor: Colors.background,
                paddingTop: insets.top,
                paddingBottom: insets.bottom,
            },
            style
            ]}
            {...props}
        />
    )
}

export default ThemedView