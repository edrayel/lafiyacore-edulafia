import { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  List,
  ListItemButton,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Divider,
  TextField,
  IconButton,
  CircularProgress,
  Badge,
} from '@mui/material';
import { Send as SendIcon } from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getConversations, getMessages, sendMessage } from './api';
import { useAuthStore } from '@/shared/stores/authStore';
import { useToastStore } from '@/shared/stores/toastStore';

export function MessagingPage() {
  const queryClient = useQueryClient();
  const { user } = useAuthStore();
  const { addToast } = useToastStore();

  const [selectedPartnerId, setSelectedPartnerId] = useState<string | null>(null);
  const [newMessage, setNewMessage] = useState('');

  // Fetch conversations
  const { data: conversations, isLoading: isLoadingConversations } = useQuery({
    queryKey: ['conversations'],
    queryFn: getConversations,
  });

  // Fetch messages for selected partner
  const { data: messages, isLoading: isLoadingMessages } = useQuery({
    queryKey: ['messages', selectedPartnerId],
    queryFn: () => getMessages(selectedPartnerId!),
    enabled: !!selectedPartnerId,
  });

  // Send message mutation
  const sendMutation = useMutation({
    mutationFn: sendMessage,
    onSuccess: () => {
      setNewMessage('');
      queryClient.invalidateQueries({ queryKey: ['messages', selectedPartnerId] });
      queryClient.invalidateQueries({ queryKey: ['conversations'] });
    },
    onError: () => {
      addToast('Failed to send message', 'error');
    },
  });

  const handleSendMessage = () => {
    if (!newMessage.trim() || !selectedPartnerId) return;

    sendMutation.mutate({
      receiver_id: selectedPartnerId,
      content: newMessage.trim(),
    });
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Box sx={{ height: 'calc(100vh - 100px)', display: 'flex', flexDirection: 'column' }}>
      <Typography variant="h4" sx={{ mb: 2 }}>
        Messages
      </Typography>

      <Paper sx={{ display: 'flex', flexGrow: 1, overflow: 'hidden' }}>
        {/* Conversations List */}
        <Box sx={{ width: 300, borderRight: 1, borderColor: 'divider', overflowY: 'auto' }}>
          {isLoadingConversations ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
              <CircularProgress />
            </Box>
          ) : (
            <List sx={{ p: 0 }}>
              {conversations?.map((conv) => (
                <div key={conv.user_id}>
                  <ListItemButton
                    sx={{ cursor: 'pointer' }}
                    selected={selectedPartnerId === conv.user_id}
                    onClick={() => setSelectedPartnerId(conv.user_id)}
                  >
                    <ListItemAvatar>
                      <Badge color="error" badgeContent={conv.unread_count}>
                        <Avatar alt={`User ${conv.user_id.substring(0, 8)}`}>{conv.user_id.substring(0, 2)}</Avatar>
                      </Badge>
                    </ListItemAvatar>
                    <ListItemText
                      primary={`User ${conv.user_id.substring(0, 8)}`}
                      secondary={conv.last_message.content}
                      secondaryTypographyProps={{
                        noWrap: true,
                        sx: { fontWeight: conv.unread_count > 0 ? 'bold' : 'normal' },
                      }}
                    />
                  </ListItemButton>
                  <Divider />
                </div>
              ))}
              {(!conversations || conversations.length === 0) && (
                <Box sx={{ p: 3, textAlign: 'center' }}>
                  <Typography color="textSecondary">No conversations yet</Typography>
                </Box>
              )}
            </List>
          )}
        </Box>

        {/* Message Thread */}
        <Box sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
          {selectedPartnerId ? (
            <>
              {/* Messages Area */}
              <Box
                sx={{
                  flexGrow: 1,
                  overflowY: 'auto',
                  p: 2,
                  display: 'flex',
                  flexDirection: 'column',
                }}
              >
                {isLoadingMessages ? (
                  <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
                    <CircularProgress />
                  </Box>
                ) : (
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, mt: 'auto' }}>
                    {messages
                      ?.slice()
                      .reverse()
                      .map((msg) => {
                        const isMe = msg.sender_id === user?.id;
                        return (
                          <Box
                            key={msg.id}
                            sx={{
                              alignSelf: isMe ? 'flex-end' : 'flex-start',
                              maxWidth: '70%',
                              bgcolor: isMe ? 'primary.main' : 'grey.200',
                              color: isMe ? 'primary.contrastText' : 'text.primary',
                              p: 1.5,
                              borderRadius: 2,
                              borderTopRightRadius: isMe ? 0 : 2,
                              borderTopLeftRadius: isMe ? 2 : 0,
                            }}
                          >
                            <Typography variant="body1">{msg.content}</Typography>
                            <Typography
                              variant="caption"
                              sx={{ opacity: 0.7, display: 'block', mt: 0.5, textAlign: 'right' }}
                            >
                              {new Date(msg.created_at).toLocaleTimeString([], {
                                hour: '2-digit',
                                minute: '2-digit',
                              })}
                            </Typography>
                          </Box>
                        );
                      })}
                  </Box>
                )}
              </Box>

              {/* Input Area */}
              <Box
                sx={{
                  p: 2,
                  borderTop: 1,
                  borderColor: 'divider',
                  display: 'flex',
                  gap: 1,
                  alignItems: 'center',
                }}
              >
                <TextField
                  fullWidth
                  variant="outlined"
                  placeholder="Type a message..."
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  size="small"
                  multiline
                  maxRows={4}
                />
                <IconButton
                  color="primary"
                  aria-label="Send message"
                  onClick={handleSendMessage}
                  disabled={!newMessage.trim() || sendMutation.isPending}
                >
                  <SendIcon />
                </IconButton>
              </Box>
            </>
          ) : (
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                height: '100%',
              }}
            >
              <Typography color="textSecondary">
                Select a conversation to start messaging
              </Typography>
            </Box>
          )}
        </Box>
      </Paper>
    </Box>
  );
}
