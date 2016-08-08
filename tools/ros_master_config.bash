#################################################################################################################################
# This BASH file sets the ROS Master IP. When no input arguments are passed, this machine is considered to run the ROS Master 	#
# and the wlan0 network interface will be used to find this machine IP. When there is one input argument, it can be the network	#
# interface name or the ROS Master IP. When there are two input arguments, one must be the network interface name and the other #
# one must be the ROS Master IP. In this last case, the order does not matter.							#
#																#
# $INTERFACE: network interface        												#
# $MASTER_IP: machine embedded master IP 											#
#																#
#																#
# Usage Examples:														#
#																#
#	$ source ~/.ros_master_config.bash # sets this PC to master using wlan0 network interface IP				#
#	$ source ~/.ros_master_config.bash 192.168.0.181 # sets master to the input IP machine using wlan0 network interface IP	#
#	$ source ~/.ros_master_config.bash eth0 # sets this PC to master using wlan0 network interface IP			#
#	$ source ~/.ros_master_config.bash eth0 192.168.0.110 									#
#	$ source ~/.ros_master_config.bash 192.168.0.191 eth0  									#
#								  								#
#################################################################################################################################
# Created on: 03/19/2015                                             								#
# Author: Adriano Henrique Rossette Leite (adrianohrl@gmail.com) 								#
# Maintainer: Expertinos UNIFEI (expertinos.unifei@gmail.com)        								#
#################################################################################################################################




##Getting my IP according to my NIC name
INTERFACES=$(ls /sys/class/net) # lists all NIC names
NUMBER_OF_INTERFACES=$( echo "$INTERFACES" | wc -l )
if [ "$NUMBER_OF_INTERFACES" -le 1 ]
then 
	echo "There is none network interface available!!!"
	return "$NUMBER_OF_INTERFACES"
fi
for INTERFACE in $INTERFACES
do
	if [ -n "$1" -a "$1" = "$INTERFACE" ] || [ -n "$2" -a "$2" = "$INTERFACE" ]
	then
		break
  	fi
	
done
BEGIN=$(/sbin/ifconfig | grep -n "$INTERFACE" | awk -F: '{print $1}' | awk 'NR==1')
END=$(/sbin/ifconfig | wc -l)
MY_IP=$(/sbin/ifconfig | tail -n "$(expr "$END" - "$BEGIN")" | grep "inet addr" | awk -F: '{print $2}' | awk '{print $1}' | awk 'NR==1')

MASTER_IP="$MY_IP"
if [ -n "$1" ]
then
	INITIAL="$(echo "$1" | head -c 1)"
	if [ -z "${INITIAL##[0-9]}" ]
	then
		MASTER_IP="$1"
	elif [ -n "$2" ]
	then
		INITIAL="$(echo "$2" | head -c 1)"
		if [ -z "${INITIAL##[0-9]}" ]
		then
			MASTER_IP="$2"
		fi
	fi
fi

export ROS_MASTER_URI=http://"$MASTER_IP":11311/
export ROS_IP="$MY_IP"
#export ROS_HOSTNAME=$(hostname)

export | grep ROS_MASTER_URI
export | grep ROS_IP
#export | grep ROS_HOSTNAME

