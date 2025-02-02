import sys
import argparse
from misc import *
from BrainDQN import *
import torch.cuda

parser = argparse.ArgumentParser(description='DQN demo for flappy bird')

parser.add_argument('--train', action='store_true', default=False,
                    help='If set true, train the model; otherwise, play game with pretrained model')
parser.add_argument('--cuda', action='store_true', default=False,
                    help='If set true, with cuda enabled; otherwise, with CPU only')
parser.add_argument('--lr', type=float, help='learning rate', default=0.0001)
parser.add_argument('--gamma', type=float,
                    help='discount rate', default=0.99)
parser.add_argument('--batch_size', type=int,
                    help='batch size', default=32)
parser.add_argument('--memory_size', type=int,
                    help='memory size for experience replay', default=5000)
parser.add_argument('--init_e', type=float,
                    help='initial epsilon for epsilon-greedy exploration',
                    default=1.0)
parser.add_argument('--final_e', type=float,
                    help='final epsilon for epsilon-greedy exploration',
                    default=0.1)
parser.add_argument('--observation', type=int,
                    help='random observation number in the beginning before training',
                    default=100)
parser.add_argument('--exploration', type=int,
                    help='number of exploration using epsilon-greedy policy',
                    default=10000)
parser.add_argument('--max_episode', type=int,
                    help='maximum episode of training',
                    default=20000)
parser.add_argument('--weight', type=str,
                    help='weight file name for finetuning(Optional)', default='')
parser.add_argument('--save_checkpoint_freq', type=int,
                    help='episode interval to save checkpoint', default=2000)

if __name__ == '__main__':
    '''
    解析传入参数，针对部分情况给出错误信息
    '''
    args = parser.parse_args()
    if args.cuda and not torch.cuda.is_available():
        print('CUDA is not available, maybe you should not set --cuda')
        sys.exit(1)
    if not args.train and args.weight == '':
        print('When test, a pretrained weight model file should be given')
        sys.exit(1)
    if args.cuda:
        print('With GPU support!')
    # 训练环境。如果给定了预训练模型，则在指定模型的基础上继续训练，否则从头开始训练一个模型
    if args.train:
        model = BrainDQN(epsilon=args.init_e,
                         mem_size=args.memory_size, cuda=args.cuda)
        resume = not args.weight == ''
        train_dqn(model, args, resume)
    # 非训练环境。必须给定一个预训练模型。
    else:
        play_game(args.weight, args.cuda, True)
