import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  FlatList,
  Alert,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';

export default function TasksScreen() {
  const [tasks, setTasks] = useState([
    { id: 1, title: 'Review journal entries', completed: false, priority: 'high', date: '2024-01-15' },
    { id: 2, title: 'Update mood tracker', completed: true, priority: 'medium', date: '2024-01-14' },
    { id: 3, title: 'Backup entries to cloud', completed: false, priority: 'low', date: '2024-01-20' },
    { id: 4, title: 'Reflect on weekly goals', completed: false, priority: 'high', date: '2024-01-17' },
  ]);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [filter, setFilter] = useState('all');

  const handleAddTask = () => {
    if (newTaskTitle.trim()) {
      setTasks([...tasks, {
        id: Math.max(...tasks.map(t => t.id), 0) + 1,
        title: newTaskTitle,
        completed: false,
        priority: 'medium',
        date: new Date().toISOString().split('T')[0],
      }]);
      setNewTaskTitle('');
      Alert.alert('Success', 'Task added successfully!');
    }
  };

  const handleToggleTask = (id) => {
    setTasks(tasks.map(task => 
      task.id === id ? { ...task, completed: !task.completed } : task
    ));
  };

  const handleDeleteTask = (id) => {
    setTasks(tasks.filter(task => task.id !== id));
  };

  const filteredTasks = tasks.filter(task => {
    if (filter === 'completed') return task.completed;
    if (filter === 'pending') return !task.completed;
    return true;
  });

  const completedCount = tasks.filter(t => t.completed).length;
  const pendingCount = tasks.filter(t => !t.completed).length;

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#999';
    }
  };

  return (
    <View style={styles.container}>
      <ScrollView>
        <View style={styles.section}>
          <Text style={styles.title}>Tasks</Text>
          <View style={styles.statsRow}>
            <View style={styles.statBox}>
              <Text style={styles.statValue}>{pendingCount}</Text>
              <Text style={styles.statLabel}>Pending</Text>
            </View>
            <View style={styles.statBox}>
              <Text style={styles.statValue}>{completedCount}</Text>
              <Text style={styles.statLabel}>Completed</Text>
            </View>
            <View style={styles.statBox}>
              <Text style={styles.statValue}>{Math.round((completedCount / tasks.length) * 100) || 0}%</Text>
              <Text style={styles.statLabel}>Progress</Text>
            </View>
          </View>
        </View>

        <View style={styles.section}>
          <View style={styles.addTaskContainer}>
            <TextInput
              style={styles.addTaskInput}
              placeholder="Add new task..."
              placeholderTextColor="#999"
              value={newTaskTitle}
              onChangeText={setNewTaskTitle}
              onSubmitEditing={handleAddTask}
              returnKeyType="send"
            />
            <TouchableOpacity style={styles.addButton} onPress={handleAddTask}>
              <MaterialCommunityIcons name="plus-circle" size={24} color="#57b8d9" />
            </TouchableOpacity>
          </View>
        </View>

        <View style={styles.section}>
          <View style={styles.filterButtons}>
            {['all', 'pending', 'completed'].map((filterType) => (
              <TouchableOpacity
                key={filterType}
                style={[
                  styles.filterButton,
                  filter === filterType && styles.filterButtonActive,
                ]}
                onPress={() => setFilter(filterType)}
              >
                <Text
                  style={[
                    styles.filterButtonText,
                    filter === filterType && styles.filterButtonTextActive,
                  ]}
                >
                  {filterType.charAt(0).toUpperCase() + filterType.slice(1)}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        <View style={styles.tasksContainer}>
          {filteredTasks.length > 0 ? (
            filteredTasks.map((task) => (
              <View key={task.id} style={styles.taskCard}>
                <TouchableOpacity
                  style={styles.taskCheckbox}
                  onPress={() => handleToggleTask(task.id)}
                >
                  <MaterialCommunityIcons
                    name={task.completed ? 'checkbox-marked' : 'checkbox-blank-outline'}
                    size={24}
                    color={task.completed ? '#10b981' : '#ccc'}
                  />
                </TouchableOpacity>
                <View style={styles.taskContent}>
                  <Text
                    style={[
                      styles.taskTitle,
                      task.completed && styles.taskTitleCompleted,
                    ]}
                  >
                    {task.title}
                  </Text>
                  <View style={styles.taskMeta}>
                    <View
                      style={[
                        styles.priorityBadge,
                        { backgroundColor: getPriorityColor(task.priority) + '20' },
                      ]}
                    >
                      <MaterialCommunityIcons
                        name="flag"
                        size={12}
                        color={getPriorityColor(task.priority)}
                      />
                      <Text style={[
                        styles.priorityText,
                        { color: getPriorityColor(task.priority) },
                      ]}>
                        {task.priority}
                      </Text>
                    </View>
                    <Text style={styles.taskDate}>{task.date}</Text>
                  </View>
                </View>
                <TouchableOpacity
                  onPress={() => handleDeleteTask(task.id)}
                >
                  <MaterialCommunityIcons name="delete" size={20} color="#f59e0b" />
                </TouchableOpacity>
              </View>
            ))
          ) : (
            <View style={styles.emptyState}>
              <MaterialCommunityIcons name="checkbox-marked-outline" size={48} color="#ccc" />
              <Text style={styles.emptyText}>
                {filter === 'completed' ? 'No completed tasks yet' : 'No pending tasks'}
              </Text>
            </View>
          )}
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  section: {
    backgroundColor: '#fff',
    padding: 16,
    marginVertical: 8,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 16,
  },
  statsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  statBox: {
    flex: 1,
    backgroundColor: '#f9f9f9',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginHorizontal: 4,
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#57b8d9',
  },
  statLabel: {
    fontSize: 11,
    color: '#999',
    marginTop: 4,
  },
  addTaskContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  addTaskInput: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#e0e0e0',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 14,
    color: '#333',
  },
  addButton: {
    padding: 8,
  },
  filterButtons: {
    flexDirection: 'row',
    gap: 8,
  },
  filterButton: {
    flex: 1,
    paddingVertical: 8,
    paddingHorizontal: 12,
    borderRadius: 8,
    backgroundColor: '#f0f0f0',
    alignItems: 'center',
  },
  filterButtonActive: {
    backgroundColor: '#57b8d9',
  },
  filterButtonText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#999',
  },
  filterButtonTextActive: {
    color: '#fff',
  },
  tasksContainer: {
    paddingHorizontal: 8,
    paddingBottom: 16,
  },
  taskCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 12,
    marginVertical: 6,
    flexDirection: 'row',
    alignItems: 'center',
    borderLeftWidth: 4,
    borderLeftColor: '#57b8d9',
  },
  taskCheckbox: {
    marginRight: 12,
  },
  taskContent: {
    flex: 1,
  },
  taskTitle: {
    fontSize: 14,
    fontWeight: '500',
    color: '#333',
    marginBottom: 6,
  },
  taskTitleCompleted: {
    textDecorationLine: 'line-through',
    color: '#999',
  },
  taskMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  priorityBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
    gap: 4,
  },
  priorityText: {
    fontSize: 10,
    fontWeight: '600',
    textTransform: 'capitalize',
  },
  taskDate: {
    fontSize: 10,
    color: '#999',
  },
  emptyState: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 40,
    backgroundColor: '#f9f9f9',
    borderRadius: 12,
    marginTop: 16,
  },
  emptyText: {
    fontSize: 14,
    color: '#999',
    marginTop: 8,
  },
});
